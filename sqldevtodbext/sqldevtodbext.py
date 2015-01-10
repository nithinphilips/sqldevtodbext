# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

"""sqldevtodbext.sqldevtodbext: provides entry point main()."""


__version__ = "0.1.0"

import argparse
import logging

from argh import ArghParser, completion, set_default_command

from .sqldevfileparser import parse

# These arguments are used by this global dispatcher and each individual
# stand-alone commands.
COMMON_PARSER = argparse.ArgumentParser(add_help=False)
COMMON_PARSER.add_argument('--debug',
                           action='store_true',
                           default=False,
                           help="Enable debug logging.")

TEMPLATE = ("\"SQL Developer Connection Profile: {ConnName}\n"
            "let g:dbext_default_profile_{ConnNameSafe} = "
            "'"
            "type=ORA:srvname={srvname}"
            ":user={user}:passwd={password}"
            ":cmd_terminator=;"
            "'")

def main():
    """
    Main entry-point for the application
    """
    parser = ArghParser(parents=[COMMON_PARSER])
    set_default_command(parser, sqldevtodbext)
    completion.autocomplete(parser)

    # Parse ahead
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s: %(message)s'
        )
    parser.dispatch()


def sqldevtodbext(filename, password="password"):
    """
    Converts a SQL Developer Connection.xml file to
    DbExt connection profiles
    """
    for connection in parse(filename, password):
        if connection.RaptorConnectionType == "Oracle":
            yield TEMPLATE.format(**connection)

