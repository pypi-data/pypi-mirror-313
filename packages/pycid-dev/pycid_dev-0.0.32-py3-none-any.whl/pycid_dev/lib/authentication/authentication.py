#!/usr/bin/python3
import datetime
import http.client
import json
import os
import uuid
from typing import Optional

from loguru import logger


class FailedLoadingAuthFileException(Exception):
    """
    If we cant load the auth file for some reason.
    """

    def __init__(self, message="Unknown", errors={}):
        super().__init__(message)
        self.errors = errors


kEpoch = datetime.datetime.utcfromtimestamp(0)


def unix_time_now_seconds():
    return (datetime.datetime.utcnow() - kEpoch).total_seconds()


# An interface that all Authentication flavors should follow
class AuthenticationInterface(object):
    def get_headers(self) -> dict:
        raise Exception("Unimplemented")

    def get_payload(self) -> dict:
        raise Exception("Unimplemented")

    def refresh(self) -> bool:
        raise Exception("Unimplemented")


# Define a class that does not include any authentication
class NoAuthentication(AuthenticationInterface):
    def __init__(self, authenticated_user_id, client_tag: Optional[int] = None):
        self._authenticated_user_id = authenticated_user_id
        self._client_tag = client_tag

    def get_headers(self):
        return {}

    def get_payload(self):
        # Populate things that the backend requires.
        # TODO it would be cool to make these optional maybe
        return {
            # This is bypassing any authentication so we can say that this is an authenticated user
            "authenticated_user_id": self._authenticated_user_id,
            "original_uid": self._authenticated_user_id,
            "is_third_party": True,  # Note: we might need to fix this.
            "remote_ip": "",  # Note: we might need to fix this.
            "timestamp_id": self._client_tag if self._client_tag else 0,
        }

    def refresh(self):
        return True


class FirebaseAuthentication(AuthenticationInterface):
    def __init__(
        self,
        auth_path: str = "./auth.json",
        auth_file_lock_path: str = "./auth.lock",
        firebase_config_path: Optional[str] = None,
    ):
        # If we were not provided with a firebase config, then look for the config in environment variables.
        FIREBASE_CONFIG = {
            # trunk-ignore(gitleaks/gcp-api-key)
            "apiKey": "AIzaSyDKAuaWu9qPNHU0Y9gACRDv3Esj6T8w3kE",
            "authDomain": "canarid-621aa.firebaseapp.com",
            "databaseURL": "https://canarid-621aa.firebaseio.com",
            "storageBucket": "",
        }
        self._firebase_config = (
            firebase_config_path if firebase_config_path else FIREBASE_CONFIG
        )
        self._auth_path = auth_path
        self._auth_file_lock_path = auth_file_lock_path

        # Default other internal variables
        self._firebase = None

        # Call into more setup
        self._init_more()

    # ##############################################################################
    # Public API
    # ##############################################################################

    def get_headers(self):
        return {"Authorization": "Bearer " + self.get_secret_token_id()}

    def get_payload(self):
        return {}

    def refresh(self):
        #
        # Try to load up the file
        #
        try:
            (
                self._access_token,
                self._refresh_token,
                self.expire_time_s,
            ) = self._load_file()
        except FailedLoadingAuthFileException as e:
            e_str = str(e)
            raise FailedLoadingAuthFileException(
                f"Failed to read authentication file. Please run the authentication refresh with 'generate' option generate a new third-party token and authentication file. - {e_str}"
            )

        #
        # If it looks like the timer for expiration has passed or is close, ask for a refresh
        #
        if unix_time_now_seconds() - self.expire_time_s > 60 * 50:
            logger.debug("Refreshing token...")
            refresh_result = self._firebase.auth().refresh(self._refresh_token)
            logger.debug("Updating locally stored credentials...")
            self._write_file(
                refresh_result["idToken"],
                refresh_result["refreshToken"],
                unix_time_now_seconds(),
            )
            return True
        else:
            logger.debug(
                "Looks like the token has been refreshed recently enough. not refreshing"
            )
            return False

    def get_secret_token_id(self):
        return self._access_token

    def generate_new(self):
        custom_token = input(
            "Please use the web interface to generate a new token. Paste it here: "
        )

        logger.debug("Retreiving updated credentials...")
        custom_token_result = self._firebase.auth().sign_in_with_custom_token(
            custom_token
        )

        access_token = custom_token_result["idToken"]
        refresh_token = custom_token_result["refreshToken"]
        # note this is okay to store this here, we're just optimizing the refresh query
        expire_time_s = unix_time_now_seconds()

        self._write_file(access_token, refresh_token, expire_time_s)

    # ##############################################################################
    # Detail API
    # ##############################################################################

    def _init_more(self):
        logger.debug(
            f"Loading authentication - reading {os.path.abspath(self._auth_path)}"
        )

        # If the auth path does not exist, then we need to generate a new one
        if not os.path.exists(self._auth_path):
            logger.warning("No authentication file found. Please generate.")

        # Cached file deets
        self._access_token = None
        self._refresh_token = None
        self.expire_time_s = None

        logger.debug("Loading authentication: Done")

    def _write_file(self, access_token, refresh_token, expire_time_s):
        """
        This creates or overwrites the authentication file.

        Note: To mitigate multiple threads/processes interacting with the file,
        we write to a unique temporary file and swap that into the true path.
        This relies on the OS/python's lib atomicity using os.replace()
        """
        # Write the contents to a unique file in the same folder
        folder_path = os.path.split(self._auth_path)[0]
        temp_file_path = os.path.join(folder_path, f"{uuid.uuid4()}.tmp")
        with open(temp_file_path, "w") as temp_auth_file:
            json.dump(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "expire_time_s": expire_time_s,
                },
                temp_auth_file,
            )

        # Now, let atomically swap in our temporary updated auth file
        try:
            os.replace(temp_file_path, self._auth_path)
        except Exception as e:
            logger.error(f"Failed to refresh authentication file, {e}")

    def _load_file(self):
        """
        Try to load details from the authentication file

        :raises FailedLoadingAuthFileException
        """
        if not os.path.exists(self._auth_path):
            raise FailedLoadingAuthFileException(
                f"File does not exist: {self._auth_path}"
            )

        with open(self._auth_path) as auth_file:
            try:
                keys = json.load(auth_file)
                access_token = keys["access_token"]
                refresh_token = keys["refresh_token"]
                expire_time_s = keys["expire_time_s"]
                return access_token, refresh_token, expire_time_s
            except:
                raise FailedLoadingAuthFileException(
                    f"Corrupt: could not read required keys: {self._auth_path}"
                )


class Auth0Authentication(AuthenticationInterface):
    def __init__(
        self,
        auth_domain: str,
        auth_path: str = "./auth.json",
        auth_file_lock_path: str = "./auth.lock",
    ):
        self._auth_domain = auth_domain
        self._auth_path = auth_path
        self._auth_file_lock_path = auth_file_lock_path

        # Default other internal variables

        # Call into more setup
        self._init_more()

    # ##############################################################################
    # Public API
    # ##############################################################################

    def get_headers(self):
        return {"Authorization": "Bearer " + self.get_secret_token_id()}

    def get_payload(self):
        return {}

    def refresh(self):
        #
        # Try to load up the file
        #
        try:
            (
                self._access_token,
                self._refresh_token,
                self.expire_time_s,
            ) = self._load_file()
        except FailedLoadingAuthFileException as e:
            e_str = str(e)
            raise FailedLoadingAuthFileException(
                f"Failed to read authentication file. Please run the authentication refresh with 'generate' option generate a new third-party token and authentication file. - {e_str}"
            )

        def refresh_access_token():
            # Per https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow/call-your-api-using-the-authorization-code-flow#authorize-user
            client_id = "pFHbmcrJrGjEVSciVps5aaJp7KfyUkWk"
            refresh_token = self._refresh_token
            token_url = f"{self._auth_domain}/oauth/token"

            # Data to send to Auth0
            data = {
                "grant_type": "refresh_token",
                "client_id": client_id,
                "refresh_token": refresh_token,
            }

            new_access_token = None
            new_expire_time_s = None
            r = None
            try:

                conn = http.client.HTTPSConnection(self._auth_domain.split("://")[1])
                payload = f"grant_type=refresh_token&client_id={client_id}&refresh_token={refresh_token}"
                headers = {
                    "content-type": "application/x-www-form-urlencoded",
                }

                conn.request("POST", token_url, payload, headers)

                res = conn.getresponse()
                data = res.read()
                # Grab response as json. Grab access_token and expires_in
                r = json.loads(data)

                new_access_token = r["access_token"]
                new_expire_time_s = unix_time_now_seconds() + r["expires_in"]
            except Exception as e:
                print(r)
                print("Failed to refresh access token:", str(e))
                return (None, None)

            return (new_access_token, new_expire_time_s)

        #
        # If it looks like the timer for expiration has passed or is close, ask for a refresh
        #
        if unix_time_now_seconds() - self.expire_time_s > 60 * 50:
            logger.debug("Refreshing token...")
            fresh_access_token, new_expire_time_s = refresh_access_token()
            if fresh_access_token is None or new_expire_time_s is None:
                logger.error("Failed to refresh token")
                return False

            logger.debug("Updating locally stored credentials...")
            self._write_file(
                fresh_access_token,
                self._refresh_token,
                new_expire_time_s,
            )
            return True
        else:
            logger.debug(
                "Looks like the token has been refreshed recently enough. not refreshing"
            )
            return False

    def get_secret_token_id(self):
        return self._access_token

    # ##############################################################################
    # Detail API
    # ##############################################################################

    def _init_more(self):
        logger.debug(
            f"Loading authentication - reading {os.path.abspath(self._auth_path)}"
        )

        # If the auth path does not exist, then we need to generate a new one
        if not os.path.exists(self._auth_path):
            logger.warning("No authentication file found. Please generate.")

        # Cached file deets
        self._access_token = None
        self._refresh_token = None
        self.expire_time_s = None

        logger.debug("Loading authentication: Done")

    def _write_file(self, access_token, refresh_token, expire_time_s):
        """
        Creates or overwrites the authentication file.

        Note: To mitigate multiple threads/processes interacting with the file,
        we write to a unique temporary file and swap that into the true path.
        This relies on the OS/python's lib atomicity using os.replace()
        """
        # Write the contents to a unique file in the same folder
        folder_path = os.path.split(self._auth_path)[0]
        temp_file_path = os.path.join(folder_path, f"{uuid.uuid4()}.tmp")
        with open(temp_file_path, "w") as temp_auth_file:
            json.dump(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "expire_time_s": expire_time_s,
                },
                temp_auth_file,
            )

        # Now, let atomically swap in our temporary updated auth file
        try:
            os.replace(temp_file_path, self._auth_path)
        except Exception as e:
            logger.error(f"Failed to refresh authentication file, {e}")

    def _load_file(self):
        """
        Try to load details from the authentication file.

        :raises FailedLoadingAuthFileException
        """
        if not os.path.exists(self._auth_path):
            raise FailedLoadingAuthFileException(
                f"File does not exist: {self._auth_path}"
            )

        with open(self._auth_path) as auth_file:
            try:
                keys = json.load(auth_file)
                access_token = keys["access_token"]
                refresh_token = keys["refresh_token"]
                expire_time_s = keys["expire_time_s"]
                return access_token, refresh_token, expire_time_s
            except:
                raise FailedLoadingAuthFileException(
                    f"Corrupt: could not read required keys: {self._auth_path}"
                )


# class Authentication(object):
#     # The default configuration for

#     kAuthPath = "./auth.json"
#     kAuthFileLockPath = "./auth.lock"

#     def printifv(self, msg):
#         if self._verbose:
#             print(f"[Authentication] {msg}")

#     def __init__(
#         self,
#         generate_new: bool = False,
#         verbose: bool = False,
#         auth_path: str = kAuthPath,
#         skip_refresh_on_init=False,
#     ):
#         """
#         Constructor
#         :param generate_new: Will prompt the user to create a new third-party token rather than refreshing an existing one.
#         :param verbose: If we should display extra info
#         :param auth_path: Path to the locally cached authentication information
#         :param skip_refresh_on_init: By default we refresh the token if needed upon object construction
#         """
#         self._auth_path = auth_path if auth_path else self.kAuthPath
#         self._verbose = verbose

#         self.printifv(f"Loading authentication from {os.path.abspath(self._auth_path)}")

#         self._firebase = pyrebase.initialize_app(self.FIREBASE_CONFIG)

#         # Cached file deets
#         self._access_token = None
#         self._refresh_token = None
#         self.expire_time_s = None

#         # #
#         # # If the user requested to generate a new third-party token/file. Help em out dude.
#         # #
#         # if generate_new:
#         #     self._generate_new()

#         # ^ TODO add this support somewhere. maybe a dedicated file. idk

#         #
#         # Do the typical refreshing now (load file, if time is past then refresh the file)
#         #
#         if not skip_refresh_on_init:
#             self.refresh()

#         self.printifv("Complete.")

#     # ##############################################################################
#     # Public API
#     # ##############################################################################

#     def refresh(self):
#         #
#         # Try to load up the file
#         #
#         try:
#             (
#                 self._access_token,
#                 self._refresh_token,
#                 self.expire_time_s,
#             ) = self._load_file()
#         except FailedLoadingAuthFileException as e:
#             e_str = str(e)
#             raise FailedLoadingAuthFileException(
#                 f"Failed to read authentication file. Please run the authentication refresh with 'generate' option generate a new third-party token and authentication file. - {e_str}"
#             )

#         #
#         # If it looks like the timer for expiration has passed or is close, ask for a refresh
#         #
#         if unix_time_now_seconds() - self.expire_time_s > 60 * 50:
#             self.printifv("Refreshing token...")
#             refresh_result = self._firebase.auth().refresh(self._refresh_token)
#             self.printifv("Updating locally stored credentials...")
#             self._write_file(
#                 refresh_result["idToken"],
#                 refresh_result["refreshToken"],
#                 unix_time_now_seconds(),
#             )
#             return True
#         else:
#             self.printifv(
#                 "Looks like the token has been refreshed recently enough. not refreshing"
#             )
#             return False

#     def get_secret_token_id(self):
#         return self._access_token

#     # ##############################################################################
#     # Private Helpers
#     # ##############################################################################
#     def _generate_new(self):
#         custom_token = input(
#             "Please use https://REDACTED to generate a new token. Paste it here: "
#         )

#         self.printifv("Retreiving updated credentials...")
#         custom_token_result = self._firebase.auth().sign_in_with_custom_token(
#             custom_token
#         )

#         access_token = custom_token_result["idToken"]
#         refresh_token = custom_token_result["refreshToken"]
#         # note this is okay to store this here, we're just optimizing the refresh query
#         expire_time_s = unix_time_now_seconds()

#         self._write_file(access_token, refresh_token, expire_time_s)
