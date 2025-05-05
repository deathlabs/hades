"""Defines a RabbitMQ client."""

# Standard library imports.
from typing import Callable

# Local imports.
from .exchange import RabbitMQExchange
from .broker import RabbitMQBroker


class RabbitMQClient:
    def __init__(
        self,
        broker: RabbitMQBroker,
        exchange: str,
        handler: Callable
    ):
        # TODO: add text to explain what this code block does.
        self.broker = broker

        # TODO: add text to explain what this code block does.
        self.handler = handler

        # TODO: add text to explain what this code block does.
        self.exchange = RabbitMQExchange(
            name=exchange,
            broker=self.broker,   
            handler=self.handler
        )