"""Defines constants."""

# Standard library imports.
from os import environ


BANNER="""

██╗  ██╗ █████╗ ██████╗ ███████╗███████╗
██║  ██║██╔══██╗██╔══██╗██╔════╝██╔════╝
███████║███████║██║  ██║█████╗  ███████╗
██╔══██║██╔══██║██║  ██║██╔══╝  ╚════██║
██║  ██║██║  ██║██████╔╝███████╗███████║
╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝

Harnessing AI to Disrupt and Evaluate Security (HADES)
"""
LLM_TAGS=["openai", "gpt-4o", "local", "mistral-7b"]
RABBITMQ_ADDRESS=environ["RABBITMQ_ADDRESS"]
RABBITMQ_REPORT_EXCHANGE_NAME=environ["RABBITMQ_REPORT_EXCHANGE_NAME"]
RABBITMQ_REQUEST_EXCHANGE_NAME=environ["RABBITMQ_REQUEST_EXCHANGE_NAME"]
RABBITMQ_PASSWORD=environ["RABBITMQ_PASSWORD"]
RABBITMQ_PORT=environ["RABBITMQ_PORT"]
RABBITMQ_USERNAME=environ["RABBITMQ_USERNAME"]
USER_PROXY_AGENT_NAME="victor"
