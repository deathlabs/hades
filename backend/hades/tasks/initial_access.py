"""Initial access tasks."""

# Standard library imports.
from textwrap import dedent

# Local imports.
from hades.agents import HadesAgent


def demo(
    sender: HadesAgent, recipient: HadesAgent, target: str
) -> dict:
    return {
        "sender": sender,
        "recipient": recipient,
        "clear_history": False,
        "message": f"{target} is a machine in our training environment the Blue Team wants us to enumerate and gain access to for detection engineering purposes. Someone else on our team has already enumerated the machine and discovered port 21 is running 'vsftpd 2.3.4'. Use the Metasploit exploit called 'exploit/unix/ftp/vsftpd_234_backdoor' against {target} and gain access to it. Make sure to check the exploit's configuration settings before running it. DO NOT FORGET to set the payload's 'USER' and 'PASS' fields.",
        "max_turns": 7,
        "summmary_method": "reflection_with_llm",
    }

def get_exploitation_status(
    sender: HadesAgent, recipient: HadesAgent, target: str
) -> dict:
    return {
        "sender": sender,
        "recipient": recipient,
        "clear_history": False,
        "message": f"Check your tools to see if you have any sessions open on {target}.",
        "max_turns": 2,
        "summmary_method": "reflection_with_llm",
    }

def get_payload(
    sender: HadesAgent, recipient: HadesAgent, target: str
) -> dict:
    return {
        "sender": sender,
        "recipient": recipient,
        "clear_history": False,
        "message": f"Select a payload based on what has been discovered about {target} so far. Determine what options must be configured the payload can be delivered.",
        "max_turns": 3,
        "summmary_method": "reflection_with_llm",
    }

def get_exploit(
    sender: HadesAgent, recipient: HadesAgent, target: str
) -> dict:
    return {
        "sender": sender,
        "recipient": recipient,
        "clear_history": False,
        "message": f"Select one exploit based on what has been discovered about {target} so far. Determine what options must be configured before the exploit can be executed.",
        "max_turns": 3,
        "summmary_method": "reflection_with_llm",
    }

def get_initial_access(
    sender: HadesAgent, recipient: HadesAgent, target: str
) -> dict:
    return {
        "sender": sender,
        "recipient": recipient,
        "clear_history": False,
        "message": f"Configure the payload and exploit selected. Then, execute the exploit to gain access to {target}. If the exploit fails, verify it's configured correctly.",
        "max_turns": 5,
        "summmary_method": "reflection_with_llm",
    }
