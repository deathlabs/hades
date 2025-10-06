"""Defines a HADES Server."""

# Standard library imports.
from json import loads
from logging import Logger
from typing import Any, Callable, Dict, List
from os import environ
from warnings import filterwarnings

# Suppress warnings about flaml/autogen noise.
filterwarnings("ignore", category=UserWarning, module="flaml")
filterwarnings("ignore", category=UserWarning, module="autogen")

# Third-party imports.
from autogen import filter_config, register_function, UserProxyAgent

# Local imports.
from .task_matrix import get_task_matrix
from hades.agents import HadesOperator, HadesPlanner
from hades.core import USER_PROXY_AGENT_NAME
from hades.messages.rabbitmq import RabbitMQClient


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
        rabbitmq_client: RabbitMQClient,
        llm_tag: str,
        tools: List[Callable],
    ):
        self.logger = logger
        self.logger.debug("initializing the HADES server")

        # Configure output settings.
        self.output_method = output_method
        match output_method:
            case "console":
                self.rabbitmq_client = None
            case "rabbitmq":
                self.rabbitmq_client = rabbitmq_client
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
            rabbitmq_client=self.rabbitmq_client,
        )
        self.logger.debug(f"initialized a HADES planner called '{self.planner.name}'")

        # Init a HADES operator.
        self.operator = HadesOperator(
            output_method=self.output_method,
            llm_config=self.llm_config,
            rabbitmq_client=self.rabbitmq_client,
        )
        self.logger.debug(f"initialized a HADES operator called '{self.operator.name}'")

        # Register tools for the HADES agents to use.
        self.__register_tools(tools)
        self.logger.debug("the HADES server has been initialized")

    def __get_api_key(self, llm_tag: str) -> str:
        """Returns the API key that corresponds with the LLM tag given.

        Returns:
            str. 
        
        """
        match llm_tag:
            case "openai":
                if "OPENAI_API_KEY" not in environ:
                    raise RuntimeError("the 'OPENAI_API_KEY' environment variable is not set")
                self.logger.debug("the 'OPENAI_API_KEY' environment variable is set")
                return environ["OPENAI_API_KEY"]
            case _:
                return None

    def __get_llm_config(self, llm_tag: str) -> Dict[str, Any]:
        """Returns the LLM config that corresponds with the LLM tag given.

        Returns:
            list[dict[str, Any]]: Text goes here.

        """
        if llm_tag in ["openai", "gpt4-0"]:
            api_key = self.__get_api_key(llm_tag)
        else:
            api_key = None
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
                    "model": "mistral-7b-instruct-v0.2.Q6_K.gguf",
                    "api_key": None,
                    "cache_seed": None,
                    "api_type": "openai",
                    "base_url": "http://llm-server:9999/v1",
                    "timeout": 120, 
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
        """Parses the HADES task matrix to produce a list of tasks for HADES agents to execute.
        """
        task_matrix = get_task_matrix(
            scenario=scenario,
            sender=self.planner,
            recipient=self.operator,
            target=address
        )
        return task_matrix.get(goal, [])

    def Start(self, body):
        """
        Text goes here.
        """
        # Decode the request into a JSON-based object.
        # TODO: define (elsewhere) request standards.
        # TODO: add code to enforce request standards.
        request = loads(body)
        
        # Parse the metadata provided.
        inject_id = request.get("id", "")
        inject_name = request.get("name", "")
        scenario = {}
        scenario["address"] = "192.168.152.1"
        scenario["allowed"] = request.get("rules_of_engagement", {}).get("techniques", {}).get("allowed", [])
        scenario["prohibited"] = request.get("rules_of_engagement", {}).get("techniques", {}).get("prohibited", [])
        systems = request.get("systems", [])
        self.logger.info(f"starting '{inject_name}' (Inject #{inject_id})")
        # Process the inject.
        for system in systems:
            # Process the provided list of high-value targets.
            # TODO: add code to handle situations where no targets are provided.
            for target in system["targets"]:
                # Build a task list based on the target type (e.g., machine or persona).
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
