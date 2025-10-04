"""Defining logging."""

# Standard library imports.
from json import dumps
from logging import DEBUG, Formatter, getLogger, StreamHandler


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
    logger = getLogger(name)
    logger.setLevel(level=DEBUG)
    handler = StreamHandler()

    match format:
        case "console":
            formatter = ConsoleFormatter()
        case "json":
            formatter = JSONFormatter()
        case _:
            raise ValueError("invalid logging format option")

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

