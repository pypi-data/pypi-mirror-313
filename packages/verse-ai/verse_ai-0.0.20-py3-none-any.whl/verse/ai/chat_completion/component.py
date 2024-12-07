from __future__ import annotations

from typing import Any

from verse.core import Component, Response

from ._models import (
    ChatCompletionMessage,
    ChatCompletionResult,
    ResponseFormat,
    Stream,
    StreamOptions,
    Tool,
    ToolChoice,
)
from ._operation import ChatCompletionOperation


class ChatCompletion(Component):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def complete(
        self,
        messages: str | list[dict | ChatCompletionMessage],
        model: str | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        max_tokens: int | None = None,
        stop: str | list[str] | None = None,
        n: int | None = None,
        presence_penalty: float | None = None,
        frequency_penalty: float | None = None,
        tools: list[dict | Tool] | None = None,
        tool_choice: str | dict | ToolChoice | None = None,
        parallel_tool_calls: bool | None = None,
        response_format: dict | ResponseFormat | None = None,
        seed: int | None = None,
        **kwargs: Any,
    ) -> Response[ChatCompletionResult]:
        return self._run_internal(ChatCompletionOperation.COMPLETE, locals())

    def stream(
        self,
        messages: str | list[dict | ChatCompletionMessage],
        model: str | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        max_tokens: int | None = None,
        stop: str | list[str] | None = None,
        n: int | None = None,
        presence_penalty: float | None = None,
        frequency_penalty: float | None = None,
        tools: list[dict | Tool] | None = None,
        tool_choice: str | dict | ToolChoice | None = None,
        parallel_tool_calls: bool | None = None,
        response_format: dict | ResponseFormat | None = None,
        seed: int | None = None,
        stream_options: StreamOptions | None = None,
        **kwargs: Any,
    ) -> Response[Stream[ChatCompletionResult]]:
        return self._run_internal(ChatCompletionOperation.STREAM, locals())

    async def acomplete(
        self,
        messages: str | list[dict | ChatCompletionMessage],
        model: str | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        max_tokens: int | None = None,
        stop: str | list[str] | None = None,
        n: int | None = None,
        presence_penalty: float | None = None,
        frequency_penalty: float | None = None,
        tools: list[dict | Tool] | None = None,
        tool_choice: str | dict | ToolChoice | None = None,
        parallel_tool_calls: bool | None = None,
        response_format: dict | ResponseFormat | None = None,
        seed: int | None = None,
        **kwargs: Any,
    ) -> Response[ChatCompletionResult]:
        return await self._arun_internal(
            ChatCompletionOperation.COMPLETE, locals()
        )

    async def astream(
        self,
        messages: str | list[dict | ChatCompletionMessage],
        model: str | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        max_tokens: int | None = None,
        stop: str | list[str] | None = None,
        n: int | None = None,
        presence_penalty: float | None = None,
        frequency_penalty: float | None = None,
        tools: list[dict | Tool] | None = None,
        tool_choice: str | dict | ToolChoice | None = None,
        parallel_tool_calls: bool | None = None,
        response_format: dict | ResponseFormat | None = None,
        seed: int | None = None,
        stream_options: StreamOptions | None = None,
        **kwargs: Any,
    ) -> Response[Stream[ChatCompletionResult]]:
        return await self._arun_internal(
            ChatCompletionOperation.STREAM, locals()
        )
