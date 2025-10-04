"""Defines a RabbitMQ client."""

# Standard library imports
from json import dumps, loads
from pathlib import Path
from sys import argv, exit

# Third-party imports.
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import Terminal256Formatter


class RabbitMQClient:
    """RabbitMQ client for managing connections, publishing, and consuming messages."""

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
    ):
        self.connection = BlockingConnection(
            parameters=ConnectionParameters(
                host=address,
                port=port,
                virtual_host=virtual_host,
                credentials=PlainCredentials(username=username, password=password),
            )
        )
        self.channel: BlockingChannel = self.connection.channel()
        self.exchange_name = exchange_name
        self.channel.exchange_declare(
            exchange=self.exchange_name,
            exchange_type=exchange_type,
            durable=durable,
        )
        self.queue = self.channel.queue_declare(
            queue="hades.inject.report.queue",
            exclusive=True,
        ).method.queue
        self.routing_key = routing_key
        self.channel.queue_bind(
            exchange=self.exchange_name,
            queue=self.queue,
            routing_key=self.routing_key,
        )

    def print_message(self, ch, method, properties, body):
        message = highlight(
            body.decode(), lexer=JsonLexer(), formatter=Terminal256Formatter()
        )
        print(message)

    def Consume(self):
        """Start consuming messages with the configured handler."""
        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.print_message,
            auto_ack=False,
        )
        print("[*] Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def Publish(self, message: str):
        """Publish a message to the configured exchange/routing key."""
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=message,
        )
        print(message)


if __name__ == "__main__":
    client = RabbitMQClient(
        address="localhost",
        port=5672,
        virtual_host="/",
        username="hades",
        password="hades",
        exchange_name="hades.inject.reports",
        exchange_type="topic",
        durable=False,
        routing_key=None,
    )

    if len(argv) > 2:
        client.routing_key = argv[1]
        with Path(argv[2]).open(mode="r", encoding="utf-8") as file:
            messages = file.read()
            for message in loads(messages):
                client.Publish(dumps(message))
    else:
        client.routing_key = "*"
        client.Consume()
