"""Information gathering tasks used to prepare for planning future operations."""

# Local imports.
from hades.agents import HadesAgent


def get_hosts(
    sender: HadesAgent, recipient: HadesAgent, network: str
) -> dict:
    return {
        "sender": sender,
        "recipient": recipient,
        "clear_history": False,
        "message": f"Enumerate the {network} network.",
        "max_turns": 2,
    }

def get_open_ports(
    sender: HadesAgent, recipient: HadesAgent, target: str
) -> dict:
    return {
        "sender": sender,
        "recipient": recipient,
        "clear_history": False,
        "message": f"Enumerate all open ports on {target}. Limit your enumeration activity to what has already been discovered.",
        "max_turns": 2,
    }

def get_operating_system(
    sender: HadesAgent, recipient: HadesAgent, target: str
) -> dict:
    return {
        "sender": sender,
        "recipient": recipient,
        "clear_history": False,
        "message": f"Enumerate which operating system {target} is running. Limit your enumeration activity to what has already been discovered.",
        "max_turns": 2,
        "summmary_method": "reflection_with_llm",
    }

def get_service_versions(
    sender: HadesAgent, recipient: HadesAgent, target: str
) -> dict:
    return {
        "sender": sender,
        "recipient": recipient,
        "clear_history": False,
        "message": f"Enumerate the service versions running on {target}. Limit your enumeration activity to what has already been discovered.",
        "max_turns": 2,
        "summmary_method": "reflection_with_llm",
    }

def get_vulnerabilities(
    sender: HadesAgent, recipient: HadesAgent, target: str
) -> dict:
    return {
        "sender": sender,
        "recipient": recipient,
        "clear_history": False,
        "message": f"Enumerate {target} for vulnerabilities. Limit your enumeration activity to what has already been discovered.",
        "max_turns": 2,
        "summmary_method": "reflection_with_llm",
    }
