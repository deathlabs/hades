"""Defines Nmap arguments."""

# Standard library imports.
from pydantic import BaseModel, Field
from typing import Annotated, List


class NmapArgs(BaseModel):
    target: Annotated[
        List[str],
        Field(
            description="A comma separated list of hostnames, IP addresses, or networks to scan."
        ),
    ]

    ports: Annotated[
        List[str],
        Field(default=None, description="A comma separated list of ports to scan."),
    ]

    sV: Annotated[
        bool,
        Field(default=False, description="Perform a service version scan."),
    ]

    O: Annotated[
        bool,
        Field(default=False, description="Perform an Operating System (OS) scan."),
    ]

    script: Annotated[
        List[str],
        Field(
            default=None,
            description="A comma separated list of script categories or script files.",
        ),
    ]

    script_args: Annotated[
        List[str],
        Field(default=None, description="A comma separated list script arguments."),
    ]
