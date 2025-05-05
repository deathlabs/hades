"""Defining logging."""

# Standard library imports.
from json import dumps
from logging import DEBUG, Formatter, getLogger, StreamHandler

# Local imports.
from .utils.highlight import highlights

class JSONFormatter(Formatter):
    def format(self, event):
        log = {
            "timestamp": self.formatTime(event),
            "name": event.name,
            "level": event.levelname,
            "message": event.getMessage(),
        }
        return dumps(log)
    
class ConsoleFormatter(Formatter):
    def format(self, event):
        log = event.getMessage()
        return log

def get_logger(name: str, format: str):
    # Init a logger.
    logger = getLogger(name)

    # Set the default logging level.
    logger.setLevel(level=DEBUG)

    # Init a stream handler.
    handler = StreamHandler()

    # Determine the formatter.
    match format:
        case "console":
            formatter = ConsoleFormatter()
        case "json":
            formatter = JSONFormatter()
        case _:
            raise ValueError("invalid logging format option")
    
    # Attach the formatter to the handler.
    handler.setFormatter(formatter)

    # Attach the handler to the logger.
    logger.addHandler(handler)

    return logger

