"""Defines a HADES agent."""

# Standard library imports.
from typing import Any, Dict, Union, Tuple
import json
import warnings

# Third-party imports.
from autogen import ConversableAgent
from autogen.agentchat import Agent, chat
from autogen.io.base import IOStream
from autogen.oai.client import OpenAIWrapper

# Local imports.
from hades.core import get_timestamp
from hades.messages.rabbitmq import RabbitMQClient


class HadesAgentIOStream(IOStream):
    def __init__(self, rabbitmq_client: RabbitMQClient, output_method: str):
        # Init the report client (assuming there is one).
        self.rabbitmq_client = rabbitmq_client

        self.__output_methods = {
            "console": self.__print_to_console,
            "rabbitmq": self.__publish_to_rabbitmq,
        }
        
        # Set the output method.
        self.output_method = output_method
        if self.output_method not in self.__output_methods:
            raise ValueError("invalid output method selected")    

    def __print_to_console(self, report):
        print(report)

    def __publish_to_rabbitmq(self, report):
        self.rabbitmq_client.Publish(report)

    def print(self, report) -> None:
        json_report = json.dumps(report)
        self.__output_methods[self.output_method](json_report)

def __post_carryover_processing(chat_info: Dict[str, Any]) -> None:
    iostream = IOStream.get_default()

    if "message" not in chat_info:
        warnings.warn(
            "message is not provided in a chat_queue entry. input() will be called to get the initial message.",
            UserWarning,
        )
    print_carryover = (
        ("\n").join([chat._post_process_carryover_item(t) for t in chat_info["carryover"]])
        if isinstance(chat_info["carryover"], list)
        else chat_info["carryover"]
    )
    message = chat_info.get("message")
    if isinstance(message, str):
        print_message = message
    elif callable(message):
        print_message = "Callable: " + message.__name__
    elif isinstance(message, dict):
        print_message = "Dict: " + str(message)
    elif message is None:
        print_message = "None"
    if chat_info.get("verbose", False):
        iostream.print("Message:\n" + print_message)
        iostream.print("Carryover:\n" + print_carryover) 

chat.__post_carryover_processing = __post_carryover_processing

class HadesAgent(ConversableAgent):
    def __init__(
        self,
        output_method: str,
        rabbitmq_client: RabbitMQClient,
        *args,
        **kwargs
    ):
        # Set the IO stream.
        self.iostream = HadesAgentIOStream(
            output_method=output_method,
            rabbitmq_client=rabbitmq_client,
        )
        IOStream.set_default(stream=self.iostream)
        
        # TODO: add comment.
        super().__init__(*args, **kwargs)

    def execute_function(self, func_call, call_id: str, verbose: bool = False) -> Tuple[bool, Dict[str, str]]:
        func_name = func_call.get("name", "")
        func = self._function_map.get(func_name, None)

        is_exec_success = False
        if func is not None:
            # Extract arguments from a json-like string and put it into a dict.
            input_string = self._format_json_str(func_call.get("arguments", "{}"))
            try:
                arguments = json.loads(input_string)
            except json.JSONDecodeError as e:
                arguments = None
                content = f"Error: {e}\n The argument must be in JSON format."

            # Try to execute the function
            if arguments is not None:
                try:
                    content = func(**arguments)
                    is_exec_success = True
                except Exception as e:
                    content = f"Error: {e}"
        else:
            content = f"Error: Function {func_name} not found."

        return is_exec_success, {
            "name": func_name,
            "role": "function",
            "content": str(content),
        }

    def _print_received_message(self, message: Union[Dict, str], sender: "Agent"):
        output = {
            "sender": sender.name,
            "receiver": self.name,
            "timestamp": get_timestamp(),
        }

        message = self._message_to_dict(message)
        if message["content"] is not None:
            output["message"] = message["content"]

        if message.get("tool_responses"):
            for tool_response in message["tool_responses"]:
                self._print_received_message(tool_response, sender)
            if message.get("role") == "tool":
                return

        if message.get("role") in ["function", "tool"]:
            if message["role"] == "function":
                id_key = "name"
            else:
                id_key = "tool_call_id"
            id = message.get(id_key, "No id found")
        else:
            content = message.get("content")

            if content is not None:
                if "context" in message:
                    content = OpenAIWrapper.instantiate(
                        content,
                        message["context"],
                        self.llm_config and self.llm_config.get("allow_format_str_template", False),
                    )

            if "function_call" in message and message["function_call"]:
                output["function_call"] = []
                function_call = dict(message["function_call"])
                arguments = function_call.get("arguments", "(No arguments found)")
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    arguments = {"raw": arguments}
                output["function_call"].append({
                    "name": function_call.get("name", "(No function name found)"),
                    "arguments": arguments
                })

            if "tool_calls" in message and message["tool_calls"]:
                output["tool_calls"] = []
                for tool_call in message["tool_calls"]:
                    id = tool_call.get("id", "No tool call id found")
                    function_call = dict(tool_call.get("function", {}))
                    arguments = function_call.get("arguments", "(No arguments found)")
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        arguments = {"raw": arguments}
                    output["tool_calls"].append({
                        "id": id,
                        "name": function_call.get("name", "(No function name found)"),
                        "arguments": arguments
                    })

        if not any(k in output for k in ["message", "tool_calls", "function_call"]):
            output["message"] = "(no content)"

        self.iostream.print(output)
