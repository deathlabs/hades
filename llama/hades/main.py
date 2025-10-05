"""Defines the inference server for HADES."""

from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama

api = FastAPI(title="HADES Inference Server")

llm = Llama(
    model_path="mistral-7b-instruct-v0.2.Q6_K.gguf"
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    temperature: float = 0.7
    max_tokens: int = 256

@api.post("/v1/chat/completions")
def chat_completion(req: ChatRequest):
    prompt = "\n".join([f"{m.role}: {m.content}" for m in req.messages])
    output = llm(prompt, temperature=req.temperature, max_tokens=req.max_tokens)
    text = output["choices"][0]["text"]
    return {
        "id": "local",
        "object": "chat.completion",
        "model": req.model,
        "choices": [{"index": 0, "message": {"role": "assistant", "content": text}}],
    }

@api.get("/healthcheck")
def healthcheck():
    try:
        _ = llm("ping", max_tokens=1)
        return { "status": "OK" }
    except Exception as e:
        return { "status": str(e) }
