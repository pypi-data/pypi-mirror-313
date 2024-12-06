import asyncio
import json
import time
import uuid
import uvicorn

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Union, Any, Dict, Literal

from ._main import ai as chat_ai

def ai(*args, **kwargs):
    return chat_ai(*args, **kwargs,max_tokens=8000,temperature=0)


class Message(BaseModel):
    role: str
    content: str
    images: Optional[List[str]] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None


class ChatRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = None
    conversation: Optional[bool] = False
    stream: Optional[bool] = False
    websearch: Optional[bool] = False
    tools: Optional[List[Dict[str, Any]]] = None
    format: Optional[str] = None
    options: Optional[Dict[str, Any]] = None
    keep_alive: Optional[str] = "5m"


class GenerateRequest(BaseModel):
    model: Optional[str] = None
    prompt: Optional[str] = None
    conversation: Optional[bool] = False
    stream: Optional[bool] = False
    websearch: Optional[bool] = False
    assistant: Optional[str] = None
    raw: bool = False
    format: Optional[str] = None
    options: Optional[Dict[str, Any]] = None
    context: Optional[List[int]] = None
    template: Optional[str] = None
    system: Optional[str] = None
    keep_alive: Optional[str] = "5m"


class ChatCompletionMessage(BaseModel):
    role: Literal["system", "user", "assistant", "function", "tool"]
    content: str
    name: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatCompletionMessage]
    temperature: Optional[float] = 1.0
    top_p: Optional[float] = 1.0
    n: Optional[int] = 1
    stream: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = 0
    frequency_penalty: Optional[float] = 0
    tools: Optional[List[Dict[str, Any]]] = None
    tool_choice: Optional[Union[str, Dict[str, Any]]] = None
    user: Optional[str] = None


class ChatCompletionResponse(BaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-{int(time.time())}")
    object: str = "chat.completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]


def process_messages(messages):
    um = []
    for m in messages:
        um.append({"role": m.role, "content": m.content})
    return um

from ._const import AVAILABLE_MODELS

class UnifiedAIAPI(FastAPI):
    def __init__(self):
        super().__init__(title="Unified AI API")
        self.ai_models = AVAILABLE_MODELS
        self.setup_routes()

    async def _process_stream(self, generator):
        """Helper method to process synchronous generator in async context"""
        for chunk in generator:
            yield chunk
            await asyncio.sleep(0)

    def setup_routes(self):

        @self.get("/api/tags")
        async def list_models():
            """List available models"""
            def get_json(model):
                return {
                    "name": model,
                    "modified_at": str(time.time()),
                    "size": 32,
                    "digest": "dummy",
                    "details": {
                        "family": "unk",
                        "parameter_size": "unk"
                    }
                }
            models = [get_json(model) for model in self.ai_models]
            # models = [
            #     {
            #         "name": "Qwen/Qwen2.5-72B-Instruct",
            #         "modified_at": str(time.time()),
            #         "size": 72000000000,
            #         "digest": "qwen-72b",
            #         "details": {
            #             "family": "qwen",
            #             "parameter_size": "72B"
            #         }
            #     },
            #     {
            #         "name": "NousResearch/Hermes-3-Llama-3.1-8B",
            #         "modified_at": str(time.time()),
            #         "size": 8000000000,
            #         "digest": "hermes-8b",
            #         "details": {
            #             "family": "llama",
            #             "parameter_size": "8B"
            #         }
            #     },
            #     {
            #         "name": "Qwen/QwQ-32B-Preview",
            #         "modified_at": str(time.time()),
            #         "size": 32000000000,
            #         "digest": "qwen-qwq-32b-preview",
            #         "details": {
            #             "family": "qwen",
            #             "parameter_size": "32B"
            #         }
            #     },
            #     {
            #         "name": "Qwen/Qwen2.5-Coder-32B-Instruct",
            #         "modified_at": str(time.time()),
            #         "size": 32000000000,
            #         "digest": "qwen-coder-32b",
            #         "details": {
            #             "family": "qwen",
            #             "parameter_size": "32B"
            #         }
            #     },
            #     {
            #         "name": "microsoft/Phi-3.5-mini-instruct",
            #         "modified_at": str(time.time()),
            #         "size": 3000000000,  # Approximated size for Phi-3.5-mini
            #         "digest": "phi-3.5-mini",
            #         "details": {
            #             "family": "phi",
            #             "parameter_size": "3B"
            #         }
            #     }
            # ]
            return {"models": models}

        @self.post("/v1/chat")
        async def chat(request: ChatRequest):
            messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
            if request.stream:
                generator = ai(
                    messages_or_prompt=messages,
                    model=request.model,
                    stream=True,
                    tools=request.tools
                )
                return StreamingResponse(
                    self._process_stream(generator),
                    media_type="text/event-stream"
                )

            response = ai(
                messages_or_prompt=messages,
                model=request.model,
                stream=False,
                tools=request.tools
            )
            return {"message": {"content": response}}

        @self.post("/v1/generate")
        async def generate(request: GenerateRequest):
            if request.stream:
                generator = ai(
                    messages_or_prompt=request.prompt,
                    model=request.model,
                    stream=True
                )
                return StreamingResponse(
                    self._process_stream(generator),
                    media_type="text/event-stream"
                )

            response = ai(
                messages_or_prompt=request.prompt,
                model=request.model,
                stream=False
            )
            return {"message": {"content": response}}


        @self.post("/v1/chat/completions")
        async def create_chat_completion(request: ChatCompletionRequest):
            # Convert OpenAI-style messages to Ollama format
            ollama_messages = [
                Message(
                    role=msg.role,
                    content=msg.content,
                    tool_calls=msg.tool_calls
                ) for msg in request.messages
            ]

            # Create Ollama-style chat request
            ollama_request = ChatRequest(
                model=request.model,
                messages=ollama_messages,
                stream=request.stream,
                options={
                    "temperature": request.temperature,
                    "top_p": request.top_p,
                    "max_tokens": request.max_tokens,
                    "presence_penalty": request.presence_penalty,
                    "frequency_penalty": request.frequency_penalty
                },
                tools=request.tools
            )

            if request.stream:
                return StreamingResponse(
                    self._stream_chat_completion(ollama_request),
                    media_type="text/event-stream"
                )

            # Get response from existing chat implementation
            response = await self._chat(ollama_request,processed_messages=process_messages(request.messages))

            # Convert to OpenAI format
            return ChatCompletionResponse(
                model=request.model,
                choices=[{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response["message"]["content"]
                    },
                    "finish_reason": "stop"
                }],
                usage={
                    "prompt_tokens": response["prompt_eval_count"],
                    "completion_tokens": response["eval_count"],
                    "total_tokens": response["prompt_eval_count"] + response["eval_count"]
                }
            )

        @self.get("/v1/models")
        async def list_models():
            return {
                "object": "list",
                "data": [
                    {
                        "id": model,
                        "object": "model",
                        "created": int(time.time()),
                        "owned_by": "organization",
                        "permission": [],
                        "root": model,
                        "parent": None
                    }
                    for model in self.ai_models
                ]
            }

    async def _generate(self, request: GenerateRequest) -> Dict[str, Any]:
        # Simulate model generation
        start_time = time.time()
        response = self.get_ai_response(request.prompt,request.model)
        self.request_model_name=request.model
        response = {
            "model": request.model,
            "created_at": datetime.utcnow().isoformat(),
            "response": response,
            "done": True,
            "context": [1, 2, 3],
            "total_duration": int((time.time() - start_time) * 1e9),
            "load_duration": 1000000,
            "prompt_eval_count": len(request.prompt) if request.prompt else 0,
            "prompt_eval_duration": 100000,
            "eval_count": 100,
            "eval_duration": 900000
        }
        return response

    async def _stream_generate(self, request: GenerateRequest):
        # Simulate streaming response
        for chunk in ai(model=request.model,messages_or_prompt=request.prompt,stream=True):
            word = chunk.choices[0].delta.content
            await asyncio.sleep(0)
            response = {
                "model": request.model,
                "created_at": datetime.utcnow().isoformat(),
                "response": word,
                "done": False
            }
            yield f"data: {json.dumps(response)}\n\n"


    async def _chat(self, request: ChatRequest,processed_messages) -> Dict[str, Any]:
        # Simulate chat response
        start_time = time.time()
        ai_model_response = self.get_ai_response(processed_messages,request.model)
        response = {
            "model": request.model,
            "created_at": datetime.utcnow().isoformat(),
            "message": {
                "role": "assistant",
                "content": ai_model_response
            },
            "done": True,
            "total_duration": int((time.time() - start_time) * 1e9),
            "load_duration": 1000000,
            "prompt_eval_count": sum(len(m.content) for m in request.messages),
            "prompt_eval_duration": 100000,
            "eval_count": 100,
            "eval_duration": 900000
        }
        return response

    async def _stream_chat(self, request: ChatRequest,processed_messages):
        for chunk in ai(messages_or_prompt=processed_messages,model=request.model,stream=True
                       ,tools=request.tools):
            word = chunk.choices[0].delta.content
            await asyncio.sleep(0)
            response = {
                "model": request.model,
                "created_at": str(uuid.uuid4()),
                "message": {"role": "assistant", "content": word},
                "done": False
            }
            yield f"data: {json.dumps(response)}\n\n"

    async def _stream_chat_completion(self,request: ChatRequest):
        async for chunk in self._stream_chat(request,process_messages(request.messages)):
            data = json.loads(chunk.replace("data: ", ""))
            if data["done"]:
                continue

            yield f"""data: {json.dumps({
                'id': f"chatcmpl-{int(time.time())}",
                'object': 'chat.completion.chunk',
                'created': int(time.time()),
                'model': request.model,
                'choices': [{
                    'index': 0,
                    'delta': {
                        'role': 'assistant',
                        'content': data['message']['content']
                    },
                    'finish_reason': None
                }]
            })}\n\n"""

    async def _stream_completion(self,request: GenerateRequest):
        async for chunk in self._stream_generate(request):
            data = json.loads(chunk.replace("data: ", ""))
            if data["done"]:
                continue

            yield f"""data: {json.dumps({
                'id': f"cmpl-{int(time.time())}",
                'object': 'text_completion',
                'created': int(time.time()),
                'model': request.model,
                'choices': [{
                    'text': data['response'],
                    'index': 0,
                    'logprobs': None,
                    'finish_reason': None
                }]
            })}\n\n"""


def start_chat_server(
    host: str = "0.0.0.0",
    port: int = 11436
):
    app = UnifiedAIAPI()
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_chat_server()
