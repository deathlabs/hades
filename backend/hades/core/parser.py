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
from hades.core import (
    RABBITMQ_REPORT_EXCHANGE_NAME,
    RABBITMQ_REQUEST_EXCHANGE_NAME,
)
from hades.messages.rabbitmq import get_rabbitmq_config
from hades.server import HadesServer
from hades.tools import bash, hydra, msfconsole, nmap, ssh


def server_mode(args):
    """Runs the HADES application in server mode.

    Returns:
      int: An exit code.

    """
    try:
        output_method = "rabbitmq"
        logger = get_logger(name="hades_server", format="json")
        rabbitmq_config = get_rabbitmq_config(
            address=environ["RABBITMQ_BROKER_ADDRESS"],
            port=environ["RABBITMQ_BROKER_PORT"],
            consumer_exchange=RABBITMQ_REQUEST_EXCHANGE_NAME,
            publisher_exchange=RABBITMQ_REPORT_EXCHANGE_NAME,
        )
        server = HadesServer(
            logger=logger,
            output_method=output_method,
            rabbitmq_config=rabbitmq_config,
            llm_tag=args.llm_tag,
            tools=[nmap, msfconsole]
        )
        server.Start()
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
        rabbitmq_config = get_rabbitmq_config(
            address=environ["RABBITMQ_BROKER_ADDRESS"],
            port=environ["RABBITMQ_BROKER_PORT"],
            consumer_exchange=RABBITMQ_REPORT_EXCHANGE_NAME,
            publisher_exchange=RABBITMQ_REQUEST_EXCHANGE_NAME,
        )
        client = HadesClient(
            output_method=output_method,
            logger=logger,
            rabbitmq_config=rabbitmq_config,
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
    
def demo_mode(args) -> int:
    """Runs the HADES application in demo mode.

    Returns:
      int: An exit code.

    """
    try:
        output_method = "console"
        logger = get_logger(name="hades_server", format="console")

        # Check if the provided file exists.
        if not path.exists(args.file):
            raise ValueError(f"{args.file} not found.")
        
        # Parse the file for the cyber inject request it contains.
        with open(args.file, encoding="utf-8") as file_buffer:
            request = load(file_buffer)
        
        # Init the HADES server.
        server = HadesServer(
            logger=logger,
            output_method=output_method,
            rabbitmq_config=None,
            llm_tag=args.llm_tag,
            tools=[nmap, msfconsole]
        )
        
        # Start the demo.
        server.Demo(request)
    except ValueError as error:
        print(error)
        return EXIT_FAILURE
    except RuntimeError as error:
        print(error)
        return EXIT_FAILURE
    except RateLimitError:
        print("there was a rate limiting error (either you exceeded the quota for the API key being used or too much data sent to the LLM")
        return EXIT_FAILURE
    except KeyboardInterrupt:
        print("\nStopping...")
        return EXIT_SUCCESS

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

    # Define an argument parser for the "demo" command.
    demo_argument_parser = subparsers.add_parser(
        prog="HADES",
        description=BANNER,
        formatter_class=RawDescriptionHelpFormatter,
        name="demo"
    )
    demo_argument_parser.add_argument(
        "--llm-tag",
        default=LLM_TAGS[0],
        type=str,
        choices=LLM_TAGS,
        help=f"A tag that matches one or more LLMs currently supported by HADES.",   
    )
    demo_argument_parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="The filepath to a cyber inject request written in JSON.",
        metavar="request.json" 
    )
    demo_argument_parser.set_defaults(command=demo_mode)

    return parser
