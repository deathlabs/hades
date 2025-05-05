"""Defines a HADES Operator."""

# Standard library imports.
from typing import Any, Dict

# Local imports.
from .agent import HadesAgent
from hades.messages.rabbitmq import RabbitMQConfig


class HadesOperator(HadesAgent):
    def __init__(
        self,
        output_method: str,
        rabbitmq_config: RabbitMQConfig,
        llm_config: Dict[str, Any],
        name: str = "HADES-Operator"
    ):
        super().__init__(
            output_method=output_method,
            rabbitmq_config=rabbitmq_config,
            name=name,
            system_message="You are a penetration tester. Be concise and do not format your responses using Markdown, etc.",
            llm_config=llm_config,
            human_input_mode="NEVER",
        )
