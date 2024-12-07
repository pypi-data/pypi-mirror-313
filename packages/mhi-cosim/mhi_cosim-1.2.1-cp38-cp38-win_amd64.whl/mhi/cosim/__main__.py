"""
PSCAD-Python Cosimulation
"""

import os
import sys
import mhi.cosim


def show_version():
    """
    Display version message"
    """

    print(f"MHI Cosim Library v{mhi.cosim.VERSION}")
    print("(c) Manitoba Hydro International Ltd.")
    print()


def open_help():
    """
    Open the help document
    """

    os.startfile(os.path.join(os.path.dirname(__file__), 'mhi-cosim.chm'))


def main():
    """
    Command Line processor
    """

    args = sys.argv[1:]
    if args in ([], ['version']):
        show_version()
    elif args == ['help']:
        open_help()
    else:
        print()
        print("Usage:")
        print("    py -m mhi.cosim [subcommand]")
        print()
        print("Available subcommands:")
        print("    version   - display module version number (default)")
        print("    help      - open help for this module")
        print()


if __name__ == '__main__':
    main()
