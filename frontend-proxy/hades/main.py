import asyncio
import contextlib
import json
import time
from os import environ
from typing import Any, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pika.exceptions import StreamLostError, AMQPConnectionError
from pydantic import BaseModel, ValidationError

from hades.messages.rabbitmq import get_rabbitmq_config


class Command(BaseModel):
    type: str
    key: str | None = None
    idempotencyKey: str | None = None
    payload: dict[str, Any] = {}

class FrontendProxy:
    def __init__(self):
        self.rabbitmq = None
        self.loop: asyncio.AbstractEventLoop | None = None
        self.connected = False

    def set_loop(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop

    def connect_with_retry(self, max_retries: int = 10, base_delay: float = 1.0):
        """Try to connect to RabbitMQ with exponential backoff."""
        attempt = 0
        while True:
            try:
                environ["RABBITMQ_QUEUE_NAME"] = "gateway.ui"
                self.rabbitmq = get_rabbitmq_config(
                    address=environ.get("RABBITMQ_BROKER_ADDRESS", "localhost"),
                    port=int(environ.get("RABBITMQ_BROKER_PORT", "5672")),
                    consumer_exchange="hades.inject.reports",
                    publisher_exchange="hades.inject.requests", 
                )
                self.rabbitmq.consumer.exchange.handler = self.__request_handler
                self.connected = True
                print("[RabbitMQ] Connected successfully")
                return
            except AMQPConnectionError as e:
                attempt += 1
                delay = base_delay * (2 ** (attempt - 1))
                print(f"[RabbitMQ] Connection failed (attempt {attempt}): {e}")
                if attempt >= max_retries:
                    print("[RabbitMQ] Max retries reached, giving up.")
                    raise
                print(f"[RabbitMQ] Retrying in {delay:.1f}s...")
                time.sleep(delay)

    def __request_handler(self, ch, method, properties, body):
        """Handle messages from RabbitMQ and forward to all websockets."""
        try:
            payload = json.loads(body)
            evt = payload if isinstance(payload, dict) else {"type": "raw", "data": payload}
        except Exception:
            evt = {"type": "raw", "data": body.decode("utf-8", "ignore")}
        if self.loop:
            self.loop.create_task(broadcast(evt))

    def publish(self, cmd: Command):
        """Send a mission (command) to RabbitMQ."""
        if not self.connected:
            raise RuntimeError("RabbitMQ not connected")

        body = json.dumps(cmd.model_dump()).encode()
        rk = cmd.key or "missions.generic"
        self.rabbitmq.publisher.Publish(
            message=body,
        )

    def start(self):
        """Start consuming RabbitMQ messages (blocking)."""
        while True:
            try:
                if not self.connected:
                    self.connect_with_retry()
                self.rabbitmq.consumer.Consume()
            except StreamLostError as error:
                print(f"[RabbitMQ] Stream lost: {error}, reconnecting...")
                self.connected = False
                time.sleep(2)
            except AMQPConnectionError as error:
                print(f"[RabbitMQ] Connection error: {error}, reconnecting...")
                self.connected = False
                time.sleep(2)

websockets: Set[WebSocket] = set()
proxy = FrontendProxy()

async def broadcast(evt: dict[str, Any]):
    """Send an event to all connected WebSocket clients."""
    msg = json.dumps(evt)
    dead = []
    for ws in list(websockets):
        try:
            await ws.send_text(msg)
        except Exception:
            dead.append(ws)
    for ws in dead:
        websockets.discard(ws)

async def maybe_publish_json_to_broker(text: str) -> bool:
    """Try to parse a WebSocket message as a Command and publish to RabbitMQ."""
    try:
        data = json.loads(text)
        cmd = Command(**data)
        proxy.publish(cmd)
        return True
    except (json.JSONDecodeError, ValidationError):
        return False
    except Exception as e:
        print(f"[Proxy] Failed to publish: {e}")
        return False

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_running_loop()
    proxy.set_loop(loop)
    loop.run_in_executor(None, proxy.start)
    yield

app = FastAPI(lifespan=lifespan)

@app.websocket("/ws")
async def ws_feed(ws: WebSocket):
    await ws.accept()
    websockets.add(ws)
    try:
        while True:
            incoming = await ws.receive_text()
            print(f"[FE -> Proxy] {incoming}")

            published = await maybe_publish_json_to_broker(incoming)
            if published:
                await ws.send_json({"type": "mission.accepted"})
            else:
                await ws.send_text(f"invalid: {incoming}")
    except WebSocketDisconnect:
        pass
    finally:
        websockets.discard(ws)
