"""
PSCAD Automation Library
"""

from argparse import ArgumentParser, Namespace
from pathlib import Path

import mhi.common
from mhi.common.help import HelpCommand
from mhi.common.zipper import LibraryZipper
from mhi.pscad import VERSION
from mhi.pscad.buildtime import BUILD_TIME


def version(args: Namespace):                  # pylint: disable=unused-argument
    """Display package version info"""

    print(f"MHI PSCAD Library v{VERSION} ({BUILD_TIME})")
    print("(c) Manitoba Hydro International Ltd.")
    print()
    print(mhi.common.version_msg())


def main():
    """Main: Command Line Interface"""

    parser = ArgumentParser(prog='py -m mhi.pscad')
    parser.set_defaults(func=version)
    subparsers = parser.add_subparsers()

    updater = LibraryZipper('PSCAD', 'mhi.pscad', 'mhi.common')
    updater.add_subparser(subparsers)

    help_cmd = HelpCommand(Path(__file__).parent / 'PSCAD_AL_doc.chm')
    help_cmd.add_subparser(subparsers)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
