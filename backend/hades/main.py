"""Defines the main entrypoint for HADES."""

# Standard library imports.
from sys import exit

# Local imports.
from hades.core import get_cli_argument_parser


def main() -> int:
    """The main entrypoint for running HADES.

    Returns:
        int: An exit code.

    """
    # Init an argument parser.
    cli_argument_parser = get_cli_argument_parser()

    # Parse arguments passed through the CLI.
    args = cli_argument_parser.parse_args()

    # Execute the command selected.
    return args.command(args)

if __name__ == "__main__":
    exit(main())
