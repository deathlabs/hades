"""Defines a RabbitMQ broker."""


class RabbitMQBroker:
    def __init__(
        self,
        address: str,
        port: int,
    ):
        self.address = address
        self.port = port
