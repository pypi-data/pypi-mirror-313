from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, AsyncGenerator, Dict, Optional

from ...schemas.chat_schema import (
    ChatCompletionChunk,
    ChatCompletionRequest,
    ChatCompletionResponse,
)


@dataclass
class GenerateResult:
    """Result from generate step"""

    text: str
    token: int
    finished: bool
    prompt_tokens: int
    generation_tokens: int
    logprobs: Optional[Dict[str, Any]] = None


class BaseMLXModel(ABC):
    """Base class for chat models"""

    @abstractmethod
    async def generate(
        self,
        request: ChatCompletionRequest,
    ) -> ChatCompletionResponse:
        """Generate completion text with parameters from request"""
        pass

    async def stream_generate(
        self,
        request: ChatCompletionRequest,
    ) -> AsyncGenerator[ChatCompletionChunk, None]:
        pass
