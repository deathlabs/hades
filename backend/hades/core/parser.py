"""Defines an argument parser for the HADES application."""

# Standard library imports.
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from json import load
from os import environ, path

# Third-party imports.
from openai import RateLimitError

# Local imports.
from .constants import (
    BANNER,
    EXIT_SUCCESS,
    EXIT_FAILURE,
    LLM_TAGS,
)
from .logging import get_logger
from hades.client import HadesClient
from hades.server import HadesServer, Start


def server_mode(args):
    """Runs the HADES application in server mode.

    Returns:
      int: An exit code.

    """
    try:
        logger = get_logger(name="hades_server", format="json")
        Start()
    except KeyboardInterrupt:
        print("\nStopping...")
        return EXIT_SUCCESS
    except RuntimeError as error:
        logger.error(error)
        return EXIT_FAILURE
    except RateLimitError:
        logger.error("there was a rate limiting error (either you exceeded the quota for the API key being used or too much data sent to the LLM")
        return EXIT_FAILURE
    
def client_mode(args) -> int:
    """Runs the HADES application in client mode.

    Returns:
      int: An exit code.

    """
    try:
        output_method = "rabbitmq"
        logger = get_logger(name="hades_client", format="json")

        # Check if the provided file exists.
        if not path.exists(args.file):
            raise ValueError(f"{args.file} not found.")
        
        # Init a HADES client.
        client = HadesClient(
            output_method=output_method,
            logger=logger,
        )

        # Parses the file and submits the cyber inject request it contains.
        with open(args.file, encoding="utf-8") as file_buffer:
            request = load(file_buffer)
            client.Publish(request)
        
        # Listen for reports sent to the RabbitMQ server.
        client.Subscribe()
    except KeyboardInterrupt:
        print("\nStopping...")
        return EXIT_SUCCESS
    except ValueError as error:
        print(error)
        return EXIT_FAILURE
    
def get_cli_argument_parser() -> ArgumentParser:
    """Creates an argument parser for the HADES application's CLI.

    Returns:
        ArgumentParser: an argument parser.

    """
    parser = ArgumentParser(
        prog="HADES",
        description=BANNER,
        formatter_class=RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(
        title="commands",
        dest="command"
    )

    # Define an argument parser for the "server" command.
    server_argument_parser = subparsers.add_parser(
        prog="HADES",
        description=BANNER,
        formatter_class=RawDescriptionHelpFormatter,
        name="server"
    )
    server_argument_parser.add_argument(
        "--llm-tag",
        default=LLM_TAGS[0],
        type=str,
        choices=LLM_TAGS,
        help=f"A tag that matches one or more LLMs currently supported by HADES.",   
    )
    server_argument_parser.set_defaults(command=server_mode)

    # Define an argument parser for the "client" command.
    client_argument_parser = subparsers.add_parser(
        prog="HADES",
        description=BANNER,
        formatter_class=RawDescriptionHelpFormatter,
        name="client"
    )
    client_argument_parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="The filepath to a cyber inject request written in JSON.",
        metavar="request.json" 
    )
    client_argument_parser.set_defaults(command=client_mode)

    return parser
