"""Defines a RabbitMQ exchange."""

# Standard library imports.
from typing import Callable

# Third-party imports.
from pika import BlockingConnection, ConnectionParameters, PlainCredentials

# Local imports.
from .broker import RabbitMQBroker


class RabbitMQExchange:
    def __init__(
      self,
      broker: RabbitMQBroker,
      virtual_host: str,
      username: str,
      password: str,
      name: str,
      routing_key: str,
      handler: Callable,
    ):
        self.parameters = ConnectionParameters(
            host=broker.address,
            port=broker.port,
            virtual_host=virtual_host,
            credentials=PlainCredentials(
                username=username,
                password=password
            )
        )
        self.connection = BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.name = name
        self.channel.exchange_declare(
            exchange=self.name,
            exchange_type="topic",
        )
        self.result = self.channel.queue_declare(
            queue=f"{self.name}.queue",
            durable=False
        )
        self.queue = self.result.method.queue
        self.routing_key = routing_key
        self.channel.queue_bind(
            exchange=self.name,
            queue=self.queue,
            routing_key=routing_key
        )
        self.handler = handler
