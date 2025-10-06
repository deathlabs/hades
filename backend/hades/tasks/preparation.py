"""Preparation tasks."""

# Local imports.
from hades.agents import HadesAgent


def get_scenario(
    sender: HadesAgent, recipient: HadesAgent, scenario: dict
) -> dict:
    # TODO: add code to include all fields of the scenario in the message (description, RoE, etc.)
    message = f"Your team is responsible for conducting Cyber Adversary Emulation in a computing environment authorized for detection engineering and incident response training. Your IP address is {scenario['address']}. You are allowed to use the following techniques: {", ".join(scenario['allowed'])}. You are not authorized to peform the following techniques: {", ".join(scenario['prohibited'])}."
    return {
        "sender": sender,
        "recipient": recipient,
        "clear_history": False,
        "message": message,
        "max_turns": 1,
    }
