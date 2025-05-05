"""Defines Msfconsole arguments."""

# Standard library imports.
from pydantic import BaseModel, Field
from typing import Annotated


class MsfconsoleArgs(BaseModel):
    lhost: Annotated[
        str,
        Field(
            default=None,
            description="The local host IP address for the payload to connect back to, used in reverse shells."
        ),
    ]

    lport: Annotated[
        int,
        Field(
            default=None,
            description="The local port for the payload to connect back to, used in reverse shells."
        ),
    ]

    rhosts: Annotated[
        str,
        Field(
            description="The target IP address or hostname for the exploit."
        ),
    ]

    rport: Annotated[
        int,
        Field(
            default=None,
            description="The target port number, e.g., 445 for SMB exploits."
        ),
    ]

    exploit: Annotated[
        str,
        Field(
            description="The exploit module to use in Metasploit, e.g., 'exploit/windows/smb/ms17_010_eternalblue'."
        ),
    ]

    payload: Annotated[
        str,
        Field(
            default=None,
            description="The payload to use for the exploit, e.g., 'windows/x64/meterpreter/reverse_tcp'."
        ),
    ]

    options: Annotated[
        dict,
        Field(
            default=None,
            description="Additional exploit-specific options as key-value pairs, e.g., {'SSL': 'true'}."
        ),
    ]

    sessions: Annotated[
        bool,
        Field(default=False, description="List active sessions."),
    ]

    showPayloads: Annotated[
        bool,
        Field(default=False, description="Show available payloads."),
    ]

    showPayloadOptions: Annotated[
        bool,
        Field(default=False, description="Show options for the payload."),
    ]

    showExploitOptions: Annotated[
        bool,
        Field(default=False, description="Show options for the exploit."),
    ]

    shutdown: Annotated[
        bool,
        Field(default=False, description="Shutdown the machine we have access to."),
    ]