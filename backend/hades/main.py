"""Defines the main entrypoint for HADES."""

# Standard library imports.
import asyncio
from json import dumps
from threading import Thread
from uuid import uuid4

# Third-party imports.
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

# Local imports.
from hades.server import HadesServer
from hades.core import (
    get_logger,
    LLM_TAGS,
    RABBITMQ_ADDRESS,
    RABBITMQ_PASSWORD,
    RABBITMQ_PORT,
    RABBITMQ_REPORT_EXCHANGE_NAME,
    RABBITMQ_USERNAME,
)
from hades.messages.rabbitmq import RabbitMQClient
from hades.tools import msfconsole, nmap

logger = get_logger(name="hades", format="json")
INJECTS: dict[str, dict] = {}

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

api = FastAPI()

api.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)

@api.post("/")
async def new_inject(request: Request):
    # Tag the inject with a UUID and then, save it.
    request = await request.json()
    logger.debug(request)
    id = str(uuid4())

    # I did this so the object returned to the frontend is a list of single key/value pairs.
    # ex: [{id: inject}, {id: inject}, {id: inject}] 
    INJECTS[id] = request
    
    # I did this so the agents are sent an object containing multiple key/value pairs. 
    # ex: {id: 1234, target: x.x.x.x}.
    request["id"] = id

    # Convert the inject to JSON.
    inject = dumps(request)

    rabbitmq_client = RabbitMQClient(
        address=RABBITMQ_ADDRESS,
        port=RABBITMQ_PORT,
        virtual_host="/",
        username=RABBITMQ_USERNAME,
        password=RABBITMQ_PASSWORD,
        exchange_name=RABBITMQ_REPORT_EXCHANGE_NAME,
        exchange_type="topic",
        durable=False,
        routing_key=id,
        handler=None,
    )

    server = HadesServer(
        logger=logger,
        output_method="rabbitmq",
        rabbitmq_client=rabbitmq_client,
        llm_tag="local",
        tools=[nmap, msfconsole]
    )

    Thread(target=server.Start, args=(inject,), daemon=True).start()    
    return {"id": id}

@api.websocket("/ws/{inject_id}")
async def watch_inject(websocket: WebSocket, inject_id: str):
    await manager.connect(websocket)
    loop = asyncio.get_event_loop()

    if inject_id not in INJECTS:
        await websocket.close(code=1008, reason="Unknown inject")
        return

    def relay(ch, method, properties, body):
        asyncio.run_coroutine_threadsafe(
            websocket.send_text(body.decode()), loop
        )

    rabbitmq_client = RabbitMQClient(
        address=RABBITMQ_ADDRESS,
        port=RABBITMQ_PORT,
        virtual_host="/",
        username=RABBITMQ_USERNAME,
        password=RABBITMQ_PASSWORD,
        exchange_name=RABBITMQ_REPORT_EXCHANGE_NAME,
        exchange_type="topic",
        durable=False,
        routing_key=inject_id,
        handler=relay,
    )

    def _consume():
        try:
            rabbitmq_client.Consume()
        except Exception as error:
            asyncio.run_coroutine_threadsafe(
                websocket.send_text(error), loop
            )

    consumer_thread = Thread(target=_consume, daemon=True)
    consumer_thread.start()

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        consumer_thread.join(timeout=1)

@api.get("/")
async def list_injects():
    return INJECTS
