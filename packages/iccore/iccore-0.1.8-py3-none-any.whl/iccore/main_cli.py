#!/usr/bin/env python3

"""
This is the main entrypoint for the iccore utility
"""

import argparse
import logging

from iccore.network.cli import setup_network_parser
from iccore.filesystem.cli import setup_filesystem_parser
from iccore.version_control.cli import setup_version_control_parsers


logger = logging.getLogger(__name__)


def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry_run",
        type=int,
        default=0,
        help="Dry run script - 0 can modify, 1 can read, 2 no modify - no read",
    )
    subparsers = parser.add_subparsers(required=True)

    setup_filesystem_parser(subparsers)
    setup_network_parser(subparsers)
    setup_version_control_parsers(subparsers)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main_cli()
