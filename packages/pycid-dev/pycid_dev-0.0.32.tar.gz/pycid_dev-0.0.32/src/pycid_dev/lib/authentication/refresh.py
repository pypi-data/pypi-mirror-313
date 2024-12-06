#!/usr/bin/python3
import argparse

from pycid_dev.lib.authentication.authentication import FirebaseAuthentication


def main(args):
    auth = (
        FirebaseAuthentication()
        if not args.path
        else FirebaseAuthentication(auth_path=args.path)
    )

    if args.generate:
        auth.generate_new()
    else:
        auth.refresh()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        usage="Run this tool to refresh authentication (must be done every hour) or create authentication (using '-g')"
    )
    parser.add_argument(
        "-g",
        "--generate",
        action="store_true",
        help="Generate a new third-party token. ",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbosely.")
    parser.add_argument(
        "-p", "--path", type=str, help="Path to the authentication file."
    )
    args = parser.parse_args()

    main(args)
