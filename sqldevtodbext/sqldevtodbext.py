# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

"""sqldevtodbext.sqldevtodbext: provides entry point main()."""


__version__ = "0.1.0"

import argcomplete
import argparse
import logging
import sys
import re

from argh import ArghParser, completion, arg

from .sqldevfileparser import parse_sqldev_xml

# These arguments are used by this global dispatcher and each individual
# stand-alone commands.
COMMON_PARSER = argparse.ArgumentParser(add_help=False)
COMMON_PARSER.add_argument('--debug',
                           action='store_true',
                           default=False,
                           help="Enable debug logging.")

def main():
    parser = ArghParser(parents=[COMMON_PARSER])
    parser.add_commands(
        [
            printlines
        ]
    )
    completion.autocomplete(parser)

    # Parse ahead
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s: %(message)s'
        )

    parser.dispatch()

template = """" SQL Developer Connection Profile: {ConnName}
let g:dbext_default_profile_oracle_{ConnNameSafe} = 'type=ORA:srvname=//{hostname}\:{port}/{service}:user={user}:passwd={passwordSafe}:cmd_terminator=;'"""

def printlines(xmlfile, password):
    for connection in parse_sqldev_xml(xmlfile, password):
        if connection.RaptorConnectionType == "Oracle":
            yield template.format(**connection)

