"""Defines a HADES client."""

# Standard library imports.
from json import dumps, loads
from logging import Logger

# Local imports.
from hades.core.utils import highlights
from hades.messages.rabbitmq import RabbitMQConfig


class HadesClient():
    """Publishes cyber inject requests and subscribes to cyber inject reports."""
    def __init__(
        self,
        output_method: str,
        logger: Logger,
        rabbitmq_config: RabbitMQConfig,
    ):
        self.logger = logger

        # Configure output settings.
        self.output_method = output_method
        match output_method:
            case "console":
                pass
            case "rabbitmq":
                self.output_method = "rabbitmq"
                self.rabbitmq = rabbitmq_config
                self.rabbitmq.consumer.exchange.handler = self.__report_handler
            case _:
                raise ValueError("no output method specified")

    def __report_handler(self, ch, method, properties, body) -> None:
        """Decode the JSON object into a Python string and then print it."""
        report_object = loads(body)
        report_string = dumps(report_object, indent=4)
        report_string_in_color = highlights(report_string)
        print(report_string_in_color)

    def Publish(self, request) -> None:
        """Text goes here."""
        request = dumps(request)
        self.rabbitmq.publisher.Publish(request)

    def Subscribe(self) -> None:
        """Text goes here."""
        self.rabbitmq.consumer.Consume()
