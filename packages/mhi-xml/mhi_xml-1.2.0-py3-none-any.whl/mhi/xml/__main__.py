"""
MHI XML - Command Line Interface
"""

import os
import sys
from mhi.xml import VERSION
from mhi.xml.buildtime import BUILD_TIME

def version():
    """
    Display version message"
    """

    print(f"MHI XML Library v{VERSION} ({BUILD_TIME})")
    print("(c) Manitoba Hydro International Ltd.")


def open_help():
    """
    Open the help document
    """

    os.startfile(os.path.join(os.path.dirname(__file__), 'mhi-xml.chm'))

def main():
    """
    Command Line processor
    """

    args = sys.argv[1:]
    if args in ([], ['version']):
        version()
    elif args == ['help']:
        open_help()
    else:
        print()
        print("Usage:")
        print("    py -m mhi.xml [subcommand]")
        print()
        print("Available subcommands:")
        print("    version   - display module version number (default)")
        print("    help      - open help for this module")
        print()

if __name__ == '__main__':
    main()
