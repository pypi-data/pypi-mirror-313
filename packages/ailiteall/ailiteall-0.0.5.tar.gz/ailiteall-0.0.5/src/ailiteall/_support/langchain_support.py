from typing import Any, Dict, List, Optional, Sequence, Union, cast, Iterator, AsyncIterator, Literal
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    ChatMessage,
    FunctionMessage,
    HumanMessage,
    SystemMessage, AIMessageChunk,
)
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
from langchain_core.callbacks import CallbackManagerForLLMRun, AsyncCallbackManagerForLLMRun
from langchain_core.pydantic_v1 import Field, SecretStr, root_validator
from openai import OpenAI, AsyncOpenAI
import json

HFModelType = Literal[
    "Qwen/Qwen2.5-72B-Instruct",
    "Qwen/QwQ-32B-Preview",
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "NousResearch/Hermes-3-Llama-3.1-8B",
    "microsoft/Phi-3.5-mini-instruct",
    "meta-llama/Llama-3.1-8B-Instruct",
    "meta-llama/Llama-3.2-1B-Instruct",
    "meta-llama/Llama-3.2-3B-Instruct",
    "01-ai/Yi-1.5-34B-Chat",
    "codellama/CodeLlama-34b-Instruct-hf",
    "google/gemma-1.1-7b-it",
    "google/gemma-2-2b-it",
    "google/gemma-2-9b-it",
    "google/gemma-2b-it",
    "HuggingFaceH4/starchat2-15b-v0.1",
    "HuggingFaceH4/zephyr-7b-alpha",
    "HuggingFaceH4/zephyr-7b-beta",
    "meta-llama/Llama-2-7b-chat-hf",
    "meta-llama/Llama-3.1-70B-Instruct",
    "meta-llama/Meta-Llama-3-70B-Instruct",
    "meta-llama/Meta-Llama-3-8B-Instruct",
    "microsoft/DialoGPT-medium",
    "microsoft/Phi-3-mini-4k-instruct",
    "mistralai/Mistral-7B-Instruct-v0.2",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
    "Qwen/Qwen2.5-1.5B-Instruct",
    "Qwen/Qwen2.5-3B-Instruct",
    "tiiuae/falcon-7b-instruct",
    "uschreiber/llama3.2"
]

def _convert_message_to_dict(message: BaseMessage) -> dict:
    """Convert LangChain message to dictionary format."""
    message_dict = {"content": message.content}

    if isinstance(message, ChatMessage):
        message_dict["role"] = message.role
    elif isinstance(message, HumanMessage):
        message_dict["role"] = "user"
    elif isinstance(message, AIMessage):
        message_dict["role"] = "assistant"
    elif isinstance(message, SystemMessage):
        message_dict["role"] = "system"
    elif isinstance(message, FunctionMessage):
        message_dict["role"] = "function"
        message_dict["name"] = message.name
    else:
        raise ValueError(f"Got unknown message type: {message}")

    return message_dict


class AILiteLangChainLLM(BaseChatModel):
    """OpenAI chat models for HuggingFace."""

    model_name: HFModelType = Field(default="Qwen/Qwen2.5-72B-Instruct", description="The HF model to use.")
    temperature: float = Field(default=0.7, description="What sampling temperature to use.")
    model_kwargs: Dict[str, Any] = Field(default_factory=dict)
    openai_api_key: SecretStr = Field(default=SecretStr("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"))
    base_url: str = Field(default="https://api-inference.huggingface.co/v1/")
    max_tokens: Optional[int] = 4028
    n: int = 1
    streaming: bool = False
    client: Any = None
    async_client: Any = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = OpenAI(
            api_key=self.openai_api_key.get_secret_value(),
            base_url=self.base_url,
        )
        self.async_client = AsyncOpenAI(
            api_key=self.openai_api_key.get_secret_value(),
            base_url=self.base_url,
        )

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "ailite"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get the identifying parameters."""
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            **self.model_kwargs
        }

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        params = {
            "model": self.model_name,
            "messages": [_convert_message_to_dict(m) for m in messages],
            "temperature": self.temperature,
            "stream": True,
            **self.model_kwargs,
        }
        if stop:
            params["stop"] = stop
        if self.max_tokens:
            params["max_tokens"] = self.max_tokens

        for chunk in self.client.chat.completions.create(**params):
            if len(chunk.choices) == 0:
                continue
            choice = chunk.choices[0]
            delta_content = choice.delta.content or ""
            generation_info = {}
            if finish_reason := choice.finish_reason:
                generation_info["finish_reason"] = finish_reason
            chunk = ChatGenerationChunk(
                message=AIMessageChunk(content=delta_content),
                generation_info=generation_info or None,
            )
            yield chunk

    async def _astream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        dm = [_convert_message_to_dict(m) for m in messages]
        params = {
            "model": self.model_name,
            "messages": dm,
            "temperature": self.temperature,
            "stream": True,
            **self.model_kwargs,
        }
        if stop:
            params["stop"] = stop
        if self.max_tokens:
            params["max_tokens"] = self.max_tokens

        async for chunk in await self.async_client.chat.completions.create(**params):
            if len(chunk.choices) == 0:
                continue
            choice = chunk.choices[0]
            delta_content = choice.delta.content or ""
            generation_info = {}
            if finish_reason := choice.finish_reason:
                generation_info["finish_reason"] = finish_reason
            chunk = ChatGenerationChunk(
                message=AIMessageChunk(content=delta_content),
                generation_info=generation_info or None,
            )
            yield chunk

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        params = {
            "model": self.model_name,
            "messages": [_convert_message_to_dict(m) for m in messages],
            "temperature": self.temperature,
            "stream": False,
            "n": self.n,
            **self.model_kwargs,
        }
        if stop:
            params["stop"] = stop
        if self.max_tokens:
            params["max_tokens"] = self.max_tokens

        response = self.client.chat.completions.create(**params)

        generations = []
        for choice in response.choices:
            message = choice.message
            gen = ChatGeneration(
                message=AIMessage(content=message.content or ""),
                generation_info=dict(finish_reason=choice.finish_reason)
            )
            generations.append(gen)

        token_usage = response.usage.model_dump() if response.usage else {}

        return ChatResult(
            generations=generations,
            llm_output={
                "token_usage": token_usage,
                "model_name": self.model_name,
            }
        )

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        # For simplicity, using sync version for now
        return self._generate(messages, stop, run_manager, **kwargs)

if __name__ == '__main__':
    messages = [
        {"role": "user", "content": "Tell me a story"}
    ]
    llm = AILiteLangChainLLM(model_name="meta-llama/Llama-3.2-1B-Instruct")
    for x in llm.stream("Tell me a story"):
        print(x.content,end = "",flush=True)