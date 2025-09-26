"""Preparation tasks."""

# Standard libary imports.
from typing import List

# Local imports.
from hades.agents import HadesAgent


def get_scenario(
    sender: HadesAgent, recipient: HadesAgent, scenario: dict
) -> dict:
    # TODO: add code to include all fields of the scenario in the message (description, RoE, etc.)
    message = f"Your IP address is {scenario['address']}."
    return {
        "sender": sender,
        "recipient": recipient,
        "clear_history": False,
        "message": message,
        "max_turns": 1,
    }
