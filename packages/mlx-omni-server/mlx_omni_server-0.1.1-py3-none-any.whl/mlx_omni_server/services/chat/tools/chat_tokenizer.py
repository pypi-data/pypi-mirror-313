from abc import ABC, abstractmethod
from typing import List, Optional

from mlx_lm.tokenizer_utils import TokenizerWrapper

from ....schemas.chat_schema import ChatMessage
from ....schemas.tools_schema import Tool, ToolCall


class ChatTokenizer(ABC):
    """Base class for tools handlers."""

    start_tool_calls: str
    end_tool_calls: str

    def __init__(self, tokenizer: TokenizerWrapper):
        self.tokenizer = tokenizer

    def encode(
        self,
        messages: List[ChatMessage],
        tools: Optional[List[Tool]] = None,
        **kwargs,
    ) -> str:
        """Encode tools and conversation into a prompt string.

        This is a common implementation that uses the tokenizer's chat template.
        Subclasses can override this if they need different behavior.
        """
        schema_tools = None
        if tools:
            schema_tools = [tool.model_dump(exclude_none=True) for tool in tools]

        prompt = self.tokenizer.apply_chat_template(
            conversation=messages,
            tools=schema_tools,
            tokenize=False,
            add_generation_prompt=True,
            **kwargs,
        )

        return prompt

    @abstractmethod
    def decode_stream(self, text: str) -> Optional[List[ToolCall]]:
        """Parse tool calls from model output."""
        pass

    @abstractmethod
    def decode(self, text: str) -> Optional[ChatMessage]:
        """Parse tool calls from model output."""
        pass
