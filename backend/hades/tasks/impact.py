"""System/data manipulation, interruption, and exfiltration tasks."""

# Local imports.
from hades.agents import HadesAgent


def shutdown(
    sender: HadesAgent, recipient: HadesAgent, target: str
) -> dict:
    return {
        "sender": sender,
        "recipient": recipient,
        "clear_history": False,
        "message": f"Shutdown {target} if you were successful in gaining access to it.",
        "max_turns": 3,
        "summmary_method": "reflection_with_llm",
    }