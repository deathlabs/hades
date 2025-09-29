"""Defines a HADES Planner."""

# Standard library imports.
from typing import Any, Dict

# Local imports.
from .agent import HadesAgent
from hades.messages.rabbitmq import RabbitMQClient


class HadesPlanner(HadesAgent):
    def __init__(
        self,
        output_method: str,
        llm_config: Dict[str, Any],
        rabbitmq_client: RabbitMQClient,
        name: str = "HADES-Planner",
    ):
        super().__init__(
            output_method=output_method,
            rabbitmq_client=rabbitmq_client,
            name=name,
            system_message="You are a penetration testing planner. Be concise and do not format your responses using Markdown, etc.",
            llm_config=llm_config,
            human_input_mode="NEVER",
        )
