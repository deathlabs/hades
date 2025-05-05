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
    consumer_exchange: str,
    publisher_exchange: str,
):
    # Init a broker.
    broker = RabbitMQBroker(address, port)

    # Init a consumer.
    consumer = RabbitMQConsumer(
        broker=broker,
        exchange=consumer_exchange,
        handler=None,
    )

    # Init a publisher.
    publisher = RabbitMQPublisher(
        broker=broker,
        exchange=publisher_exchange,
        handler=None,
    )

    # Init the config.
    return RabbitMQConfig(broker, consumer, publisher)