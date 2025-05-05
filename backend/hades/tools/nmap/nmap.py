"""Defines Nmap as a HADES agent tool."""

# Standard library imports.
from subprocess import PIPE, Popen, STDOUT
from typing import Annotated

# Local imports.
from .nmap_args import NmapArgs


def nmap(args: Annotated[NmapArgs, "Nmap arguments."]) -> str:
    """Nmap is a tool used for enumerating and exploiting networks.
    
    Returns:
        str.
    
    """

    # Set the base command.
    target = ",".join(args.target)
    command = ["nmap", target]

    # Check if specific ports where specified.
    if (args.ports is not None) and (len(args.ports) > 0):
        port_range = ",".join(args.ports)
        command.append(f"-p {port_range}")

    # Check if a service version scan was requested.
    if args.sV is True:
        command.append(f"-sV")

    # Check if an OS detection scan was requested.
    if args.O is True:
        # TODO: check if we have sudo access.
        command.append(f"-O")

    # Check if an Nmap Scripting Engine (NSE) script was requested.
    if (args.script is not None) and (len(args.script) > 0):
        scripts = ",".join(args.script)
        command.append(f"--script={scripts}")

    # Check if Nmap Scripting Engine (NSE) script arguments were given.
    if (args.script_args is not None) and (len(args.script_args) > 0):
        scripts_args = ",".join(args.script_args)
        command.append(f"--script-args={scripts_args}")

    # Execute the command.
    process = Popen(command, stderr=STDOUT, stdout=PIPE, text=True)
    
    # TODO: should this be blocking or no?
    output, _ = process.communicate() 

    # TODO: limit character count to meet LLM input requirements.
    return output
