import argparse
import os.path
from pathlib import Path

from connector.__about__ import __version__
from connector.scaffold.create import scaffold, setup_args as setup_scaffold_args


def main():
    parser = argparse.ArgumentParser(description="Lumos Connectors CLI")
    parser.add_argument(
        "--version", "-v", help="Print the version of this library and exit", action="store_true"
    )

    command_subparsers = parser.add_subparsers(dest="command")
    scaffold_parser = command_subparsers.add_parser("scaffold", help="Create a new connector")
    setup_scaffold_args(scaffold_parser)

    command_subparsers.add_parser("spec", help="Print the OpenAPI spec")

    args = parser.parse_args()

    if args.version:
        print(__version__)
        return
    elif args.command == "scaffold":
        scaffold(args)
    elif args.command == "spec":
        spec_file_path = Path(os.path.dirname(__file__)) / "spec" / "openapi.yaml"
        print(spec_file_path.read_text())


if __name__ == "__main__":
    main()
