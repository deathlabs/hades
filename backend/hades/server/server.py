"""Defines a HADES Server."""

# Standard library imports.
from json import loads
from logging import Logger
from time import sleep
from typing import Any, Callable, Dict, List
from os import environ
from uuid import uuid4
from warnings import filterwarnings

# Supress warnings about flaml.automl not being installed.
filterwarnings("ignore", category=UserWarning, module="flaml")

# Supress warnings about repetitive chat recipients.
filterwarnings("ignore", category=UserWarning, module="autogen")

# Third-party imports.
from autogen import filter_config, register_function, UserProxyAgent
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pika.exceptions import StreamLostError
import uvicorn

# Local imports.
from .task_matrix import get_task_matrix
from hades.agents import HadesOperator, HadesPlanner
from hades.core import USER_PROXY_AGENT_NAME
from hades.messages.rabbitmq import RabbitMQConfig

app = FastAPI()
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
)
@app.post("/")
async def root(request: Request):
    data = await request.json()
    sleep(3)
    return {"uuid": uuid4(), "received": data, "note": "Got your mission!"}

class HadesServer:
    """Responds to cyber inject requests.
        
    Args:
        llm_tag. str.
        tools. A list of functions.
        message_client.

    """
    def __init__(
        self,
        logger: Logger,
        output_method: str,
        rabbitmq_config: RabbitMQConfig,
        llm_tag: str,
        tools: List[Callable],
    ):
        self.logger = logger
        self.logger.debug("initializing the HADES server")

        # Configure output settings.
        self.output_method = output_method
        match output_method:
            case "console":
                self.rabbitmq = None
            case "rabbitmq":
                self.rabbitmq = rabbitmq_config
                self.rabbitmq.consumer.exchange.handler = self.__request_handler
                self.logger.debug(f"will use the RabbitMQ broker at '{self.rabbitmq.broker.address}:{self.rabbitmq.broker.port}'")
                self.logger.debug(f"will use the '{self.rabbitmq.consumer.exchange.name}' exchange to consume requests")
                self.logger.debug(f"will use the '{self.rabbitmq.publisher.exchange.name}' exhange to publish reports")
            case _:
                raise ValueError("no output method specified")

        # Init an Autogen user proxy agent.
        self.user_proxy = UserProxyAgent(
            name=USER_PROXY_AGENT_NAME,
            code_execution_config={"use_docker": False}
        )

        # Parse the LLM config provided.
        self.llm_config = self.__get_llm_config(llm_tag)[0]
        self.logger.debug(f"using the '{self.llm_config['model']}' LLM")

        # Init a HADES planner.
        self.planner = HadesPlanner(
            output_method=self.output_method,
            llm_config=self.llm_config,
            rabbitmq_config=self.rabbitmq,
        )
        self.logger.debug(f"initialized a HADES planner called '{self.planner.name}'")

        # Init a HADES operator.
        self.operator = HadesOperator(
            output_method=self.output_method,
            llm_config=self.llm_config,
            rabbitmq_config=self.rabbitmq,
        )
        self.logger.debug(f"initialized a HADES operator called '{self.operator.name}'")

        # Register tools for the HADES agents to use.
        self.__register_tools(tools)
        self.logger.debug("the HADES server has been initialized")

    def __get_api_key(self, llm_tag: str) -> str:
        """
        Returns an OpenAI API key.
        """
        match llm_tag:
            case "openai":
                if "OPENAI_API_KEY" not in environ:
                    raise RuntimeError("the 'OPENAI_API_KEY' environment variable is not set")
                self.logger.debug("the 'OPENAI_API_KEY' environment variable is set")
                return environ["OPENAI_API_KEY"]
            case "camogpt":
                if "CAMOGPT_API_KEY" not in environ:
                    raise RuntimeError("the 'CAMOGPT_API_KEY' environment variable is not set")
                self.logger.debug("the 'CAMOGPT_API_KEY' environment variable is set")
                return environ["CAMOGPT_API_KEY"]
            case _:
                return None

    def __get_llm_config(self, llm_tag: str = "openai") -> Dict[str, Any]:
        """
        Returns an LLM config.
        """
        # TODO: refactor so an API key is only loaded if the 'openai' or 'gpt-4o' tags are selected.
        api_key = self.__get_api_key(llm_tag)
        return filter_config(
            config_list=[
                {
                    "tags": ["openai", "gpt-4o"],
                    "model": "gpt-4o",
                    "api_key": api_key,
                    "cache_seed": None,
                },
                {
                    "tags": ["local", "mistral-7b"],
                    "model": "mistral-7b-instruct-v0.1.Q5_K_M.gguf",
                    "api_key": api_key,
                    "api_type": "openai",
                    "base_url": "http://localhost:8000/api",
                    "cache_seed": None,
                },
            ],
            filter_dict={"tags": [llm_tag]}
        )

    def __register_tools(self, tools) -> None:
        """Registers tools for HADES agents to use.
        
        Returns:
            bool: True if all tool registrations were successful. False if all tool registrations were not successful.
        
        """
        try:
            for tool in tools:
                self.logger.debug(f"registering '{tool.__name__}' as a tool for HADES agents to use")
                register_function(
                    tool,
                    caller=self.planner,
                    executor=self.operator,
                    description=tool.__doc__,
                )
        except Exception as e:
            self.logger.error(e)
            raise RuntimeError(e)

    def __get_task_list(self, scenario: dict, address: str, goal: str) -> List[Callable]:
        """
        Parses the HADES task matrix to produce a list of tasks for HADES agents to execute.
        """
        task_matrix = get_task_matrix(
            scenario=scenario,
            sender=self.planner,
            recipient=self.operator,
            target=address
        )
        return task_matrix.get(goal, [])

    def __request_handler(self, ch, method, properties, body):
        """
        Text goes here.
        """
        # Decode the request into a JSON-based object.
        # TODO: define (elsewhere) request standards.
        # TODO: add code to enforce request standards.
        request = loads(body)
        
        # Parse the metadata provided.
        inject_id = request.get("id", 0)
        inject_name = request.get("name", "")
        scenario = request.get("scenario", {})
        systems = request.get("systems", [])
        self.logger.info(f"starting '{inject_name}' (Inject #{inject_id})")

        # Process the inject.
        for system in systems:
            # Process the provided list of high-value targets.
            # TODO: add code to handle situations where no high-value targets are provided.
            for target in system["high-value-targets"]:
                # Build a task list based on the target type (e.g., machine or user).
                match target["type"]:
                    case "machine":
                        address = target["address"]
                        goal = target["goals"][0]
                        task_list = self.__get_task_list(scenario, address, goal)
                    case _:
                        return None

            # Task the HADES agents.
            # TODO: add code to trace the following activity.
            self.user_proxy.initiate_chats(
                chat_queue=task_list,
            )
        self.logger.info(f"ending '{inject_name}' (Inject #{inject_id})")
    
    def Start(self):
        """
        Text goes here.
        """
        uvicorn.run(app, host="0.0.0.0", port=8888)

    def Demo(self, request):
        """
        Text goes here.
        """
        self.logger.info("started the HADES server")
        self.logger.info("received a request")

        # Process the systems provided.
        systems = request.get("systems", [])
        for system in systems:
            # TODO: add code to handle situations where no high-value targets are provided.

            # Process the provided list of high-value targets.
            for target in system["high-value-targets"]:
                # Build a task list based on the target type.
                match target["type"]:
                    case "machine":
                        address = target["address"]
                        goal = target["goals"][0]
                        task_list = self.__get_task_list(address, goal)
                    case _:
                        return None

            # Give the task list to the HADES agents.
            # TODO: start trace
            self.user_proxy.initiate_chats(
                chat_queue=task_list,
            )
            # TODO: end trace
        self.logger.info("finished processing the request")
