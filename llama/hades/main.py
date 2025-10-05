"""Defines the inference server for HADES."""

# Standard library imports.
import asyncio

# Third-party imports.
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_cpp import Llama

api = FastAPI(title="HADES Inference Server")

llm = Llama(model_path="mistral-7b-instruct-v0.2.Q6_K.gguf")

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    temperature: float = 0.7
    max_tokens: int = 256

@api.post("/v1/chat/completions")
async def chat_completion(request: ChatRequest):
    print(request.json())
    prompt = "\n".join([f"{message.role}: {message.content}" for message in request.messages])
    try:
        output = await asyncio.wait_for(
            asyncio.to_thread(
                llm,
                prompt,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            ),
            timeout=60,
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="LLM inference timed out")

    content = output["choices"][0]["text"]
    return {
        "id": "local",
        "object": "chat.completion",
        "model": request.model,
        "choices": [{"index": 0, "message": {"role": "assistant", "content": content}}],
    }

@api.get("/healthcheck")
def healthcheck():
    try:
        _ = llm("ping", max_tokens=1)
        return {"status": "OK"}
    except Exception as e:
        return {"status": str(e)}
