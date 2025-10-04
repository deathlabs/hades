"""Defines a RabbitMQ client."""

# Standard library imports.
from typing import Callable

# Third-party imports.
from pika import BlockingConnection, ConnectionParameters, PlainCredentials


class RabbitMQClient:
    """RabbitMQ client for managing connections, publishing, and consuming messages.

    Args:
        address (str): RabbitMQ server address.
        port (int): Port number for the RabbitMQ server.
        virtual_host (str): Virtual host to connect to.
        username (str): Username for authentication.
        password (str): Password for authentication.
        exchange_name (str): Name of the exchange to connect to.
        exchange_type (str): Type of the exchange (e.g., 'direct', 'topic', 'fanout').
        durable (bool): Whether the exchange should survive broker restarts.
        routing_key (str): Routing key for binding messages.
        handler (Callable): Function to handle consumed messages.

    Attributes:
        channel (BlockingChannel): Active channel for communication with RabbitMQ.
        exchange_name (str): Name of the configured exchange.
        queue (str): Name of the bound queue.
        routing_key (str): Routing key used for publishing/consuming.
        handler (Callable): Function used to process incoming messages.
    """
    def __init__(
        self,
        address: str,
        port: int,
        virtual_host: str,
        username: str,
        password: str,
        exchange_name: str,
        exchange_type: str,
        durable: bool,
        routing_key: str,
        handler: Callable,
    ):
        self.channel = BlockingConnection(
            parameters=ConnectionParameters(
                host=address,
                port=port,
                virtual_host=virtual_host,
                credentials=PlainCredentials(
                    username=username,
                    password=password
                )
            )
        ).channel()
        self.exchange_name = exchange_name
        self.channel.exchange_declare(
            exchange=self.exchange_name,
            exchange_type=exchange_type,
        )
        self.queue = self.channel.queue_declare(
            queue=f"{self.exchange_name}.queue",
            durable=durable
        ).method.queue
        self.routing_key = routing_key
        self.channel.queue_bind(
            exchange=exchange_name,
            queue=self.queue,
            routing_key=routing_key
        )
        self.handler = handler

    def Consume(self):
        """
        Add text to explain what this function does.
        """
        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.handler,
            auto_ack=False
        )
        self.channel.start_consuming()

    def Publish(self, message):
        """
        Add text to explain what this function does.
        """
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=message
        )
