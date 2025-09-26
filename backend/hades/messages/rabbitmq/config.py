"""Defines a RabbitMQ network."""

# Local imports
from .consumer import RabbitMQConsumer
from .publisher import RabbitMQPublisher
from .broker import RabbitMQBroker


class RabbitMQConfig:
    """A RabbitMQ configuration class.
    
    Args:
        broker (RabbitMQBroker): RabbitMQ broker used for managing the connection.
        consumer (RabbitMQConsumer): RabbitMQ consumer responsible for consuming requests.
        publisher (RabbitMQPublisher): RabbitMQ publisher responsible for publishing reports.

    Attributes:
        broker (RabbitMQBroker): RabbitMQ broker used for managing the connection.
        consumer (RabbitMQConsumer): RabbitMQ consumer responsible for consuming requests.
        publisher (RabbitMQPublisher): RabbitMQ publisher responsible for publishing reports.
        
    """
    def __init__(
        self,
        broker: RabbitMQBroker,
        consumer: RabbitMQConsumer,
        publisher: RabbitMQPublisher,
    ):
        self.broker = broker
        self.consumer = consumer
        self.publisher = publisher 

def get_rabbitmq_config(
    address: str,
    port: int,
    virtual_host: str,
    username: str,
    password: str,
    routing_key: str,
    consumer_exchange_name: str,
    publisher_exchange_name: str,
):
    broker = RabbitMQBroker(address, port)
    consumer = RabbitMQConsumer(
        broker=broker,
        virtual_host=virtual_host,
        username=username,
        password=password,
        exchange_name=consumer_exchange_name,
        routing_key=routing_key,
        handler=None,
    )
    publisher = RabbitMQPublisher(
        broker=broker,
        virtual_host=virtual_host,
        username=username,
        password=password,
        exchange_name=publisher_exchange_name,
        routing_key=routing_key,
        handler=None,
    )
    return RabbitMQConfig(broker, consumer, publisher)
