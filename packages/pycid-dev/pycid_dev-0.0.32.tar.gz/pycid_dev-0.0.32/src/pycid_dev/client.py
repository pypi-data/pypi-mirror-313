#!/usr/bin/python3
import datetime
import json
import os
import time
from typing import List, Optional

import requests
from pycid_dev.lib.authentication.authentication import (
    AuthenticationInterface,
    NoAuthentication,
)
from pycid_dev.lib.craft.craft import Craft

# Local imports
from pycid_dev.lib.tree.tree import Tree, deserialize


class QueryException(Exception):
    """
    If query to the backend fails
    """

    def __init__(self, message="Unknown", errors={}):
        super().__init__(message)
        self.errors = errors


class LocalAuthenticationException(Exception):
    """
    If local auth stuffs fails
    """

    def __init__(self, message="Unknown", errors={}):
        super().__init__(message)
        self.errors = errors


class CidClient:
    def __init__(self, backend_url, auth: AuthenticationInterface):
        """
        Constructor
        """
        self._backend_url = backend_url
        self._auth = auth

        # Some caching of some stuff
        self._user_info = None

        # TODO can I add a periodic functionality or something here to do refreshes
        self._auth.refresh()

        # # self._auth()

        # if auth_config:
        #     self.firebase = pyrebase.initialize_app(AuthConfig.PUBLIC_CONFIG)

        #     # Note: we skip the refresh on init, instead we manually call refresh, if it actually needed to refresh,
        #     #       then we will sleep a second to make sure the new token propogates through the CID backend infra.
        #     self._authentication = Authentication(
        #         verbose=True, skip_refresh_on_init=True, auth_path=path_to_auth)

        #     if self._authentication.refresh():
        #         time.sleep(0.2)  # sleeping is not ideal but should do the trick

        # self._user_info = self._fetch_user_info()

    # ##############################################################################
    # Public API
    # ##############################################################################

    def refresh_auth(self):
        self._auth.refresh()

    #
    # User information queries
    #
    def trees_info(self):
        """
        Gets the trees available and the elements that it is composed of.
        """
        if not self._user_info:
            self._user_info = self._fetch_user_info()
        return self._user_info["user"]["trees"]

    def fetch_tree(self, tree_id):
        """
        Pull all data for a tree from the network. Push it into a new Craft

        :returns A Craft object

        NOTE: this performs a network query
        """
        # Find the elements that the tree is composed of
        tree = None
        # TODO woudl be good to expose an endpoint that has just the info we need.
        for tree_info in self.trees_info():
            if tree_info["id"] == tree_id:
                tree = tree_info
        if not tree:
            raise ValueError("Provided tree id could not be found: " + tree_id)

        # Pull down all the crates associated with the tree
        # TODO might want to keep these separated? or at a minimum store a mapping from node id to crate id that it belongs to
        # Hacky, need to remove hashing/payloading from security checkpoint. Push it to backend.
        crate = None
        if isinstance(self._auth, NoAuthentication):
            crate = self._fetch_instance_crate(tree["id"])["tree_nodes_groups"]
        else:
            crate = self._fetch_instance_crate(tree["id"])[
                "tree_nodes_groups"
            ]

        # Pull down and create the tree
        the_tree = self._fetch_instance_tree(tree["id"])

        return Craft(
            self,
            tree["name"],
            tree["id"],
            crate,
            the_tree,
            #  {"component_resync_query": self._component_resync_query,
            #   "component_resync_execute": self._component_resync_execute,
            #   "component_attribute_edit": self._component_attribute_edit,
            #   "component_attribute_remove": self._component_attribute_remove,
            #   }
        )

    def get_account_info(self):
        """
        Just return the raw firebase information for the user. Maybe its a lot of info but it is not obscured anyway at the moment so just show 'em.
        """
        return self.firebase.auth().get_account_info(self._auth.get_secret_token_id())

    # ##############################################################################
    # Underlying client network requests
    # ##############################################################################

    #
    # Resync stuff
    #
    def node_resync_query(self, id, tree_id):
        """
        :param payload: The payload to attach while requesting
        """
        return self._smart_post(
            "/v1/instance/node/resync/query", payload={"id": id, "tree_id": tree_id}
        )

    def node_resync_execute(self, id, tree_id):
        """
        :param payload: The payload to attach while requesting
        """
        return self._smart_post(
            "/v1/instance/node/resync/execute", payload={"id": id, "tree_id": tree_id}
        )

    #
    # Node stuff
    #
    def rename_node(self, tree_id, node_id, name):
        """
        :param tree_id: The crate id that the node belongs to
        :param node_id: The id of the node to rename
        :param name: The new name of the node
        """
        return self._smart_post(
            "/v1/instance/node/rename",
            payload={"node_id": node_id, "new_name": name, "tree_id": tree_id},
        )

    #
    # Attribute stuff
    #
    def attribute_edit(
        self, id, attribute_name, attribute_id, value, traits, aux, tree_id
    ):
        """
        :param payload: The payload to attach while requesting
        """
        # We must note that the trait has been overridden if it was inherited.
        if "inheritance_source" in traits:
            OVERRIDDEN_KEY = "overridden"
            traits[OVERRIDDEN_KEY] = True

        return self._smart_post(
            "/v1/instance/node/attribute/edit",
            payload={
                "id": id,
                "name": attribute_name,
                "attribute_id": attribute_id,
                "value": value,
                "traits": traits,
                "aux": aux,
                "tree_id": tree_id,
            },
        )

    def attribute_value_update(self, tree_id, node_id, attribute_id, value):
        """
        :param tree_id: The tree id that the node belongs to
        :param node_id: The id of the node to with the attribute we're editing
        :param attribute_id: The id of the attribute we're editing
        :param value: The new value of the attribute
        """

        return self._smart_post(
            "/v1/instance/node/attribute/value/update",
            payload={
                "tree_id": tree_id,
                "node_id": node_id,
                "attribute_id": attribute_id,
                "value": value,
            },
        )

    def attribute_remove(self, id, attribute_id, tree_id):
        """
        :param payload: The payload to attach while requesting
        """
        return self._smart_post(
            "/v1/instance/node/attribute/remove",
            payload={"id": id, "attribute_id": attribute_id, "tree_id": tree_id},
        )

    # ##############################################################################
    # Private Helpers
    # ##############################################################################

    def _smart_post(self, end_point, payload={}):
        payload.update(
            {
                "username": "test_user",  # TODO remove this trash
                "password": "test_password",
                "isThirdParty": True,
            }
        )
        payload.update(self._auth.get_payload())
        headers = {}
        headers.update(self._auth.get_headers())

        result = requests.post(
            f"{self._backend_url}{end_point}", headers=headers, json=payload
        )
        if result.status_code != 200:
            raise QueryException(
                f"Failed to post {end_point}: {str(result.status_code)}: {result.text}"
            )

        resp = result.json()
        return resp["payload"]
    def _fetch_user_info(self):
        return self._smart_post("/v1/user/information")

    def _fetch_instance_crate(self, tree_id):
        # TODO this api is named funy}
        return self._smart_post(
            "/v1/instance/nodes",
            payload={
                "tree_ids": [tree_id],
            },
        )

    def _fetch_instance_tree(self, tree_id):
        # TODO this api is named funy}
        return self._smart_post(
            "/v1/tree/frame/query",
            payload={
                "tree_id": tree_id,
            },
        )


