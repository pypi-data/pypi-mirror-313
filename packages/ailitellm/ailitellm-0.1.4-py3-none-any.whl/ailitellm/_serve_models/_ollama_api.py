from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union, Literal
from openai import OpenAI
import time
import json
import asyncio

app = FastAPI()

client = OpenAI(
    base_url="https://api-inference.huggingface.co/v1/",
    api_key="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"
)

HFModelType = Literal[
    "Qwen/Qwen2.5-72B-Instruct",
    "Qwen/QwQ-32B-Preview",
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "NousResearch/Hermes-3-Llama-3.1-8B",
    "microsoft/Phi-3.5-mini-instruct"
]


# Request/Response Models
class GenerateRequest(BaseModel):
    model: str
    prompt: str
    stream: bool = True
    options: Optional[Dict[str, Any]] = None
    context: Optional[List[int]] = None
    format: Optional[str] = None
    raw: Optional[bool] = False


class ChatMessage(BaseModel):
    role: str
    content: str
    images: Optional[List[str]] = None


class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    stream: bool = True
    options: Optional[Dict[str, Any]] = None
    format: Optional[str] = None


class EmbeddingRequest(BaseModel):
    model: str
    input: Union[str, List[str]]
    options: Optional[Dict[str, Any]] = None


def huggingface_model(model: HFModelType):
    return model


def calculate_duration_ns():
    """Return current time in nanoseconds for duration calculations"""
    return time.time_ns()


async def stream_generate_response(response):
    """Stream the generate response in Ollama format"""
    start_time = calculate_duration_ns()

    for chunk in response:
        if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
            yield json.dumps({
                "model": response.model,
                "created_at": str(chunk.created),
                "response": chunk.choices[0].delta.content,
                "done": False
            }) + "\n"

    # Final response with metadata
    end_time = calculate_duration_ns()
    yield json.dumps({
        "model": response.model,
        "created_at": str(response.created),
        "done": True,
        "total_duration": end_time - start_time,
        "eval_count": response.usage.total_tokens if hasattr(response, 'usage') else 0
    }) + "\n"


async def stream_chat_response(response):
    """Stream the chat response in Ollama format"""
    start_time = calculate_duration_ns()

    for chunk in response:
        if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
            yield json.dumps({
                "model": response.model,
                "created_at": str(chunk.created),
                "message": {
                    "role": "assistant",
                    "content": chunk.choices[0].delta.content
                },
                "done": False
            }) + "\n"

    # Final response with metadata
    end_time = calculate_duration_ns()
    yield json.dumps({
        "model": response.model,
        "created_at": str(response.created),
        "done": True,
        "total_duration": end_time - start_time,
        "eval_count": response.usage.total_tokens if hasattr(response, 'usage') else 0
    }) + "\n"


@app.post("/api/generate")
async def generate(request: GenerateRequest):
    try:
        response = client.chat.completions.create(
            model=huggingface_model(request.model),
            messages=[{"role": "user", "content": request.prompt}],
            temperature=request.options.get('temperature', 0.7) if request.options else 0.7,
            max_tokens=request.options.get('num_predict', 2048) if request.options else 2048,
            stream=request.stream
        )

        if request.stream:
            return StreamingResponse(
                stream_generate_response(response),
                media_type="text/event-stream"
            )
        else:
            return {
                "model": response.model,
                "created_at": str(response.created),
                "response": response.choices[0].message.content,
                "done": True,
                "total_duration": calculate_duration_ns(),
                "eval_count": response.usage.total_tokens if hasattr(response, 'usage') else 0
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        response = client.chat.completions.create(
            model=huggingface_model(request.model),
            messages=messages,
            temperature=request.options.get('temperature', 0.7) if request.options else 0.7,
            max_tokens=request.options.get('num_predict', 2048) if request.options else 2048,
            stream=request.stream
        )

        if request.stream:
            return StreamingResponse(
                stream_chat_response(response),
                media_type="text/event-stream"
            )
        else:
            return {
                "model": response.model,
                "created_at": str(response.created),
                "message": {
                    "role": "assistant",
                    "content": response.choices[0].message.content
                },
                "done": True,
                "total_duration": calculate_duration_ns(),
                "eval_count": response.usage.total_tokens if hasattr(response, 'usage') else 0
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/embeddings")
async def embeddings(request: EmbeddingRequest):
    try:
        response = client.embeddings.create(
            model=huggingface_model(request.model),
            input=request.input
        )

        return {
            "embeddings": response.data[0].embedding if isinstance(request.input, str) else [d.embedding for d in
                                                                                             response.data],
            "total_duration": calculate_duration_ns()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Model Management Endpoints
@app.get("/api/tags")
async def list_models():
    """List available models"""
    models = [
        {
            "name": "Qwen/Qwen2.5-72B-Instruct",
            "modified_at": str(time.time()),
            "size": 72000000000,
            "digest": "qwen-72b",
            "details": {
                "family": "qwen",
                "parameter_size": "72B"
            }
        },
        {
            "name": "NousResearch/Hermes-3-Llama-3.1-8B",
            "modified_at": str(time.time()),
            "size": 8000000000,
            "digest": "hermes-8b",
            "details": {
                "family": "llama",
                "parameter_size": "8B"
            }
        },
        {
            "name": "Qwen/QwQ-32B-Preview",
            "modified_at": str(time.time()),
            "size": 32000000000,
            "digest": "qwen-qwq-32b-preview",
            "details": {
                "family": "qwen",
                "parameter_size": "32B"
            }
        },
        {
            "name": "Qwen/Qwen2.5-Coder-32B-Instruct",
            "modified_at": str(time.time()),
            "size": 32000000000,
            "digest": "qwen-coder-32b",
            "details": {
                "family": "qwen",
                "parameter_size": "32B"
            }
        },
        {
            "name": "microsoft/Phi-3.5-mini-instruct",
            "modified_at": str(time.time()),
            "size": 3000000000,  # Approximated size for Phi-3.5-mini
            "digest": "phi-3.5-mini",
            "details": {
                "family": "phi",
                "parameter_size": "3B"
            }
        }
    ]
    return {"models": models}

HFModelType = Literal[
    "Qwen/Qwen2.5-72B-Instruct",
    "Qwen/QwQ-32B-Preview",
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "NousResearch/Hermes-3-Llama-3.1-8B",
    "microsoft/Phi-3.5-mini-instruct"
]

def ollama_serve():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=11435)

if __name__ == "__main__":
    ollama_serve()
