"""Defines a RabbitMQ consumer."""

# Standard library imports.
from typing import Callable

# Local imports.
from .broker import RabbitMQBroker
from .exchange import RabbitMQExchange


class RabbitMQConsumer():
    def __init__(
        self,
        broker: RabbitMQBroker,
        virtual_host: str,
        username: str,
        password: str,
        exchange_name: str,
        routing_key: str,
        handler: Callable,
    ):
        self.broker = broker
        self.handler = handler
        self.exchange = RabbitMQExchange(
            broker=self.broker,
            virtual_host=virtual_host,
            username=username,
            password=password,
            name=exchange_name,
            routing_key=routing_key,
            handler=self.handler
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
