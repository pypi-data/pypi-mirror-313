from __future__ import annotations

from typing import Any

from verse.core import DataModel, OperationParser

from ._models import (
    ChatCompletionMessage,
    ResponseFormat,
    StreamOptions,
    Tool,
    ToolChoice,
)


class ChatCompletionOperationParser(OperationParser):
    def get_args(self, strong_types: bool = False) -> dict:
        args = super().get_args()
        if "messages" in args:
            if isinstance(args["messages"], str):
                args["messages"] = [
                    {
                        "role": "user",
                        "content": args["messages"],
                    }
                ]

        if not strong_types:
            for name, value in args.items():
                if isinstance(value, DataModel):
                    args[name] = value.to_dict()
                if isinstance(value, list):
                    for i, _ in enumerate(value):
                        if isinstance(value[i], DataModel):
                            value[i] = value[i].to_dict()
            return args

        types_map: dict[str, Any] = {
            "messages": ChatCompletionMessage,
            "stream_options": StreamOptions,
            "tools": Tool,
            "tool_choice": ToolChoice,
            "response_format": ResponseFormat,
        }
        for name, value in args.items():
            if name in types_map:
                if isinstance(value, list):
                    for i, _ in enumerate(value):
                        if isinstance(value[i], dict):
                            value[i] = types_map[name].from_dict(value[i])
                else:
                    if isinstance(value[i], dict):
                        args[name] = types_map[name].from_dict(value)
        return args
