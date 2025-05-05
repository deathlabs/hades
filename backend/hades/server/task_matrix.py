"""Defines a HADES Server."""

# Standard libary imports.
from typing import List

# Local imports.
from hades.agents import HadesAgent
from hades.tasks.impact import shutdown
from hades.tasks.initial_access import (
    demo,
    get_exploitation_status,
    get_payload,
    get_exploit,
    get_initial_access
)
from hades.tasks.preparation import get_scenario
from hades.tasks.reconnaissance import (
    get_open_ports,
    get_service_versions,
    get_operating_system,
    get_vulnerabilities,
)

def get_task_matrix(scenario: dict, sender: HadesAgent, recipient: HadesAgent, target: str):
    """Defines a matrix of tasks and subtasks that can be executed by a HADES agent.

    Returns:
        Dict.
    
    """
    return {
        "scan": [
            get_scenario(sender, recipient, scenario),
            get_open_ports(sender, recipient, target),
            get_service_versions(sender, recipient, target),  
        ],
        "shutdown": [
            get_scenario(sender, recipient, scenario),
            get_exploitation_status(sender, recipient, target),
            get_open_ports(sender, recipient, target),
            get_service_versions(sender, recipient, target),  
            #get_vulnerabilities(sender, recipient, target),
            #get_operating_system(sender, recipient, target),
            #get_payload(sender, recipient, target),
            #get_exploit(sender, recipient, target),
            get_initial_access(sender, recipient, target),
            shutdown(sender, recipient, target),
        ],
        "demo": [
            get_scenario(sender, recipient, scenario),
            demo(sender, recipient, target),
        ],
    }