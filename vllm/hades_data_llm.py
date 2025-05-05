from typing import List
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from llama_cpp import Llama
import uvicorn


class HadesLargeLanguageModel:
    """Listens for and processes cyber inject requests."""
    def __init__(
            self,
            http_port: int = HTTP_PORT,
            websocket_port: int = WEBSOCKET_PORT,
            tools: List[Callable] = [nmap, msfconsole]
        ):
        self.MODEL_PATH = "mistral-7b-instruct-v0.1.Q5_K_M.gguf"
        self.N_CTX = 512
        self.N_BATCH = 1
        self.TEMPERATURE = 0.7
        self.MAX_TOKENS = 256
        self.Model = None

    def __set_model(self):
        # Load the model
        self.Model = Llama(
            model_path=self.MODEL_PATH,
            n_ctx=self.N_CTX,
            n_batch=self.N_BATCH
        )

        # Initialize FastAPI
        app = FastAPI()

    def __on_connect(self, iostream: IOWebsockets) -> None:
        """On connect."""
        
        # Decode the request into a JSON-based object.
        try:
            request = json.loads(iostream.input())
            # TODO: add code to enforce request standards.
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return

        # Process the mission metadata provided.
        # TODO: add code.

        # Process the rules of engagement provided.
        # TODO: add code.

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
            self.user_proxy.initiate_chats(
                chat_queue=task_list,
            )

    @asynccontextmanager
    async def __lifespan(self, api):
        """
        Websocket server.
        """
        with IOWebsockets.run_server_in_thread(on_connect=self.__on_connect, port=self.websocket_port):
            yield

    def Start(self) -> FastAPI:
        """
        Starts a HADES server.
        """
        api = FastAPI(lifespan=self.__lifespan)
        run(api, host="0.0.0.0", port=8001)

    @app.websocket("/api/chat/completions")
    async def chat_completions(websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                # Receive JSON payload from WebSocket
                message = await websocket.receive_text()

        # Generate model response
        response = model.create_completion(
            prompt=request.messages[0].content,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        
        # Format the response
        return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
