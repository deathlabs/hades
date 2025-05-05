"""Defines a RabbitMQ consumer."""

# Standard library imports.
from typing import Callable

# Local imports.
from .broker import RabbitMQBroker
from .client import RabbitMQClient
from .exchange import RabbitMQExchange


class RabbitMQConsumer(RabbitMQClient):
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

    def Consume(self):
        """
        Add text to explain what this function does.
        """
        self.exchange.channel.basic_consume(
            queue=self.exchange.queue,
            on_message_callback=self.exchange.handler,
            auto_ack=True
        )
        self.exchange.channel.start_consuming()
