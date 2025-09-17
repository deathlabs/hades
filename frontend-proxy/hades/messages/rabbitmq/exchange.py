"""Defines a RabbitMQ exchange."""

# Standard library imports.
from os import environ
from typing import Callable

# Third-party imports.
from pika import BlockingConnection, ConnectionParameters, PlainCredentials

# Local imports.
from .broker import RabbitMQBroker


class RabbitMQExchange:
    def __init__(
      self,
      name: str,
      broker: RabbitMQBroker,
      handler: Callable
    ):
        self.name = name
        self.routing_key = self.name.split(".")[-1]
        self.parameters = ConnectionParameters(
            host=broker.address,
            port=broker.port,
            virtual_host="/",
            credentials=PlainCredentials(
                username=environ["RABBITMQ_USERNAME"],
                password=environ["RABBITMQ_PASSWORD"]
            )
        )
        self.connection = BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange_type="topic",
            exchange=self.name
        )
        self.result = self.channel.queue_declare(queue=f"{self.name}.queue", durable=True)
        self.queue = self.result.method.queue
        self.channel.queue_bind(
            exchange=self.name,
            queue=self.queue,
            routing_key=self.routing_key
        )
        self.handler = handler
