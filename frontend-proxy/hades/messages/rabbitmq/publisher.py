"""Defines a RabbitMQ client."""

# Standard library imports.
from typing import Callable

# Local imports.
from .broker import RabbitMQBroker
from .client import RabbitMQClient
from .exchange import RabbitMQExchange


class RabbitMQPublisher(RabbitMQClient):
    def __init__(
        self,
        broker: RabbitMQBroker,
        exchange: str,
        handler: Callable
    ):
        # TODO: add text to explain what this code block does.
        self.broker = broker

        # TODO: add text to explain what this code block does.
        self.exchange = RabbitMQExchange(
            name=exchange,
            broker=self.broker,   
            handler=handler
        )

    def Publish(self, message):
        """
        Add text to explain what this function does.
        """
        self.exchange.channel.basic_publish(
            exchange=self.exchange.name,
            routing_key=self.exchange.routing_key,
            body=message
        )
