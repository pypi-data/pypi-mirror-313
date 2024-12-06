"""
EasyMaker command line tool (python -m easymaker [options])
"""

import sys


def main():
    if __package__ == "":
        import os.path

        path = os.path.dirname(os.path.dirname(__file__))
        sys.path[0:0] = [path]
    from easymaker.cli import cli

    sys.exit(cli.main())


if __name__ == "__main__":
    sys.exit(main())
