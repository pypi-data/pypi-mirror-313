from __future__ import annotations

__all__ = ["Cohere"]

import json
import uuid
from typing import Any

from cohere import NonStreamedChatResponse, StreamedChatResponse
from cohere import ToolCall as CohereToolCall
from cohere import ToolResult as CohereToolResult

from verse.core import Context, NCall, Operation, Provider, Response
from verse.core.exceptions import BadRequestError

from .._helper import copy_arg
from .._models import (
    ChatCompletionMessage,
    ChatCompletionMessageContentPart,
    ChatCompletionResult,
    Choice,
    Stream,
    Tool,
    ToolCall,
    ToolCallFunction,
    Usage,
)
from .._operation import ChatCompletionOperation
from .._operation_parser import ChatCompletionOperationParser


class Cohere(Provider):
    api_key: str | None
    model: str | None
    base_url: str | None
    client_name: str | None
    timeout: float | None
    raw_prompting: bool | None
    force_single_step: bool | None
    system_message_in_preamble: bool
    nparams: dict

    _client: Any
    _aclient: Any

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "command-r-plus",
        base_url: str | None = None,
        client_name: str | None = None,
        timout: float | None = None,
        raw_prompting: bool | None = None,
        force_single_step: bool | None = None,
        system_message_in_preamble: bool = True,
        nparams: dict = dict(),
    ):
        """Initialize.

        Args:
            api_key:
                Cohere API key.
            model:
                Cohere model.
            base_url:
                Cohere base url.
            client_name:
                Cohere client name.
            timout:
                Timeout for client.
            raw_prompting:
                Whether raw prompting is enabled in every request.
            force_single_step:
                Whether single step is enabled in every request.
            system_message_in_preamble:
                Whether system message should be sent as preamble
                or sent through chat history. Defaults to True.
            nparams:
                Native params for Cohere client.
        """
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.client_name = client_name
        self.timeout = timout
        self.raw_prompting = raw_prompting
        self.force_single_step = force_single_step
        self.system_message_in_preamble = system_message_in_preamble
        self.nparams = nparams

        self._client = None
        self._aclient = None

    def init(self, context: Context | None = None) -> None:
        if self._client is not None:
            return

        from cohere import Client

        self._client = Client(**self.get_client_params())

    async def ainit(self, context: Context | None = None) -> None:
        if self._aclient is not None:
            return

        from cohere import AsyncClient

        self._aclient = AsyncClient(**self.get_client_params())

    def get_client_params(self) -> dict:
        args: dict = {}
        if self.api_key is not None:
            args["api_key"] = self.api_key
        if self.base_url is not None:
            args["base_url"] = self.base_url
        if self.client_name is not None:
            args["client_name"] = self.client_name
        if self.timeout is not None:
            args["timeout"] = self.timeout
        args = args | self.nparams
        return args

    def run(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
        **kwargs,
    ) -> Any:
        self.init(context=context)
        op_parser = ChatCompletionOperationParser(operation)
        ncall, state = self._get_ncall(
            op_parser,
            self._client,
            ClientHelper(self._client),
        )
        if ncall is None:
            return super().run(operation=operation, context=context, **kwargs)
        nresult = ncall.invoke()
        result = self._convert_nresult(
            nresult,
            state,
            op_parser,
        )
        return Response(result=result, native=dict(call=ncall, result=nresult))

    async def arun(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
        **kwargs,
    ) -> Any:
        await self.ainit(context=context)
        op_parser = ChatCompletionOperationParser(operation)
        ncall, state = self._get_ncall(
            op_parser,
            self._aclient,
            AsyncClientHelper(self._aclient),
        )
        if ncall is None:
            return await super().arun(
                operation=operation, context=context, **kwargs
            )
        nresult = await ncall.ainvoke()
        result = self._convert_nresult(
            nresult,
            state,
            op_parser,
        )
        return Response(result=result, native=dict(call=ncall, result=nresult))

    def _get_ncall(
        self,
        op_parser: ChatCompletionOperationParser,
        client: Any,
        client_helper: Any,
    ) -> tuple[NCall | None, dict]:
        call = None
        state: dict = {}
        nargs = op_parser.get_nargs()
        op_converter = OperationConverter(
            self.model,
            self.raw_prompting,
            self.force_single_step,
            self.system_message_in_preamble,
        )
        # COMPLETE
        if op_parser.op_equals(ChatCompletionOperation.COMPLETE):
            args, state = op_converter.convert_complete(
                op_parser.get_args(strong_types=True)
            )
            call = NCall(
                client.chat,
                args,
                nargs,
            )
        # STREAM
        elif op_parser.op_equals(ChatCompletionOperation.STREAM):
            args, state = op_converter.convert_stream(
                op_parser.get_args(strong_types=True)
            )
            call = NCall(
                client_helper.stream,
                {"args": args, "nargs": nargs},
            )
        return call, state

    def _convert_nresult(
        self,
        nresult: Any,
        state: dict,
        op_parser: ChatCompletionOperationParser,
    ) -> Any:
        result: Any = None
        result_converter = ResultConverter()
        # COMPLETE
        if op_parser.op_equals(ChatCompletionOperation.COMPLETE):
            result = result_converter.convert_complete_result(
                nresult,
                state,
            )
        # STREAM
        if op_parser.op_equals(ChatCompletionOperation.STREAM):
            result = result_converter.convert_stream_result(
                nresult,
                state,
            )
        return result


class ClientHelper:
    client: Any

    def __init__(self, client: Any):
        self.client = client

    def stream(self, args: dict, nargs: Any):
        return NCall(
            self.client.chat_stream,
            args,
            nargs,
        ).invoke()


class AsyncClientHelper:
    client: Any

    def __init__(self, client: Any):
        self.client = client

    async def stream(self, args: dict, nargs: Any):
        return NCall(
            self.client.chat_stream,
            args,
            nargs,
        ).invoke()


class ResultConverter:
    _generation_id: str
    _model: str

    def __init__(self):
        pass

    def convert_complete_result(
        self,
        nresult: NonStreamedChatResponse,
        state: dict,
    ) -> ChatCompletionResult:
        choice = Choice(
            finish_reason=self._convert_finish_reason(nresult.finish_reason),
            index=0,
            message=ChatCompletionMessage(
                role="assistant",
                content=nresult.text,
                tool_calls=self._convert_tool_calls(nresult.tool_calls),
            ),
        )
        return ChatCompletionResult(
            id=nresult.generation_id,
            choices=[choice],
            usage=self._convert_usage(nresult),
            model=state["model"],
        )

    def convert_stream_result(
        self,
        nresult: Any,
        state: dict,
    ) -> Stream:
        self._model = state["model"]
        return Stream(nresult, self.convert_stream_chunk)

    def convert_stream_chunk(
        self, chunk: StreamedChatResponse
    ) -> ChatCompletionResult:
        if chunk.event_type == "stream-start":
            self._generation_id = chunk.generation_id
            result = ChatCompletionResult(
                id=self._generation_id,
                choices=[
                    Choice(
                        index=0, delta=ChatCompletionMessage(role="assistant")
                    )
                ],
                model=self._model,
            )
        elif chunk.event_type == "text-generation":
            result = ChatCompletionResult(
                id=self._generation_id,
                choices=[
                    Choice(
                        index=0,
                        delta=ChatCompletionMessage(
                            role="assistant", content=chunk.text
                        ),
                    )
                ],
                model=self._model,
            )
        elif chunk.event_type == "tool-calls-generation":
            result = ChatCompletionResult(
                id=self._generation_id,
                choices=[
                    Choice(
                        index=0,
                        delta=ChatCompletionMessage(
                            role="assistant",
                            content=chunk.text,
                            tool_calls=self._convert_tool_calls(
                                chunk.tool_calls
                            ),
                        ),
                    )
                ],
                model=self._model,
            )
        elif chunk.event_type == "stream-end":
            result = ChatCompletionResult(
                id=self._generation_id,
                choices=[
                    Choice(
                        finish_reason=self._convert_finish_reason(
                            chunk.finish_reason
                        ),
                        index=0,
                        delta=ChatCompletionMessage(),
                    )
                ],
                model=self._model,
                usage=self._convert_usage(chunk.response),
            )
        return result

    def _convert_tool_calls(
        self, tool_calls: list[CohereToolCall] | None
    ) -> list[ToolCall] | None:
        if tool_calls is None:
            return None
        rtool_calls = []
        for tool_call in tool_calls:
            rtool_calls.append(
                ToolCall(
                    id=str(uuid.uuid4()),
                    function=ToolCallFunction(
                        name=tool_call.name,
                        arguments=json.dumps(tool_call.parameters),
                    ),
                )
            )
        return rtool_calls

    def _convert_finish_reason(self, finish_reason: str | None) -> str | None:
        finish_reason_map = {
            "COMPLETE": "stop",
            "STOP_SEQUENCE": "stop",
            "MAX_TOKENS": "length",
            "ERROR_TOXIC": "content_filter",
            "ERROR": "error",
            "ERROR_LIMIT": "error",
            "USER_CANCEL": "cancel",
            None: None,
        }
        return finish_reason_map[finish_reason]

    def _convert_usage(self, nresult: NonStreamedChatResponse) -> Usage | None:
        usage = None
        if (
            nresult.meta is not None
            and nresult.meta.billed_units is not None
            and nresult.meta.billed_units.input_tokens is not None
            and nresult.meta.billed_units.output_tokens is not None
        ):
            usage = Usage(
                completion_tokens=int(nresult.meta.billed_units.output_tokens),
                prompt_tokens=int(nresult.meta.billed_units.input_tokens),
                total_tokens=int(
                    nresult.meta.billed_units.input_tokens
                    + nresult.meta.billed_units.output_tokens
                ),
            )
        return usage


class OperationConverter:
    model: str | None
    raw_prompting: bool | None
    force_single_step: bool | None
    system_message_in_preamble: bool

    def __init__(
        self,
        model: str | None,
        raw_prompting: bool | None,
        force_single_step: bool | None,
        system_message_in_preamble: bool,
    ):
        self.model = model
        self.raw_prompting = raw_prompting
        self.force_single_step = force_single_step
        self.system_message_in_preamble = system_message_in_preamble

    def convert_complete(
        self,
        args: dict,
    ) -> tuple[dict, dict]:
        return self._convert_args(args)

    def convert_stream(
        self,
        args: dict,
    ) -> tuple[dict, dict]:
        return self._convert_args(args)

    def _convert_args(
        self,
        args: dict,
    ) -> tuple[dict, dict]:
        state: dict = {}
        role_map: dict = {
            "user": "USER",
            "assistant": "CHATBOT",
            "system": "SYSTEM",
            "tool": "TOOL",
        }
        rargs: dict = {}
        if "model" not in args or args["model"] is None:
            rargs["model"] = self.model
        else:
            copy_arg(args, rargs, "model")
        state["model"] = rargs["model"]
        chat_history: list = []
        tool_calls = []
        single_step_tool_results = []
        messages: list[ChatCompletionMessage] = args["messages"]
        for message in messages:
            chat_message: dict = {}
            chat_message["role"] = role_map[message.role]
            if message.tool_calls:
                tool_calls.extend(message.tool_calls)
                chat_message["tool_calls"] = self._convert_tool_calls(
                    message.tool_calls
                )
            if isinstance(message.content, str):
                chat_message["text"] = message.content
            elif isinstance(message.content, list):
                parts: list[ChatCompletionMessageContentPart] = message.content
                text = ""
                for part in parts:
                    if part.type == "text":
                        text = f"{text} {part.text}"
                    else:
                        raise BadRequestError(
                            "Chat message type not supported"
                        )
                chat_message["text"] = text
            if (
                chat_message["role"] == "SYSTEM"
                and self.system_message_in_preamble
            ):
                rargs["preamble"] = chat_message["text"]
            elif (
                chat_message["role"] == "CHATBOT"
                and message.tool_calls is not None
                and self.force_single_step
            ):
                pass
            elif chat_message["role"] == "TOOL":
                tool_results = []
                for tool_call in tool_calls:
                    if tool_call.id == message.tool_call_id:
                        outputs: list = []
                        if isinstance(message.content, str):
                            try:
                                json_object = json.loads(message.content)
                                if isinstance(json_object, dict):
                                    outputs.append(json_object)
                                elif isinstance(json_object, list):
                                    outputs.extend(json_object)
                            except ValueError:
                                outputs.append({"result": message.content})
                        else:
                            raise BadRequestError(
                                "Tool output should be encoded as a string"
                            )
                        tool_results.append(
                            CohereToolResult(
                                call=self._convert_tool_call(tool_call),
                                outputs=outputs,
                            )
                        )
                if not self.force_single_step:
                    chat_message["tool_results"] = tool_results
                    chat_history.append(chat_message)
                else:
                    single_step_tool_results = tool_results
            else:
                chat_history.append(chat_message)
        last_message = chat_history[-1]
        if last_message["role"] == "USER":
            rargs["message"] = last_message["text"]
            if len(chat_history) >= 2:
                rargs["chat_history"] = chat_history[:-1]
        elif last_message["role"] == "TOOL":
            # It will come here only for multi-step.
            rargs["tool_results"] = chat_message["tool_results"]
            rargs["message"] = ""
            if len(chat_history) >= 2:
                rargs["chat_history"] = chat_history[:-1]
        else:
            raise BadRequestError("Last message should be user or tool role")
        if len(chat_history) >= 2:
            rargs["chat_history"] = chat_history[:-1]
        copy_arg(args, rargs, "temperature")
        copy_arg(args, rargs, "max_tokens")
        copy_arg(args, rargs, "seed")
        copy_arg(args, rargs, "presence_penalty")
        copy_arg(args, rargs, "frequency_penalty")
        copy_arg(args, rargs, "top_p", "p")
        copy_arg(args, rargs, "top_k", "k")
        if "stop" in args:
            rargs["stop_sequences"] = (
                [args["stop"]]
                if isinstance(args["stop"], str)
                else args["stop"]
            )
        if "response_format" in args:
            rargs["response_format"] = {"type": args["response_format"].type}
        if "tools" in args:
            rargs["tools"] = self._convert_tools(args["tools"])
        if len(single_step_tool_results) > 0:
            rargs["tool_results"] = single_step_tool_results
        if self.raw_prompting:
            rargs["raw_prompting"] = self.raw_prompting
        if self.force_single_step:
            rargs["force_single_step"] = self.force_single_step
        copy_arg(args, rargs, "force_single_step", "force_single_step")
        request_options = self._convert_request_options(args)
        if request_options:
            args["request_options"] = request_options
        return rargs, state

    def _convert_request_options(self, args: dict) -> dict | None:
        request_options = {}
        if "timeout" in args:
            request_options["timeout_in_seconds"] = int(args["timeout"])
        if "extra_headers" in args:
            copy_arg(
                args, request_options, "extra_headers", "additional_headers"
            )
        if "extra_query" in args:
            copy_arg(
                args,
                request_options,
                "extra_query",
                "additional_query_parameters",
            )
        if "extra_body" in args:
            copy_arg(
                args,
                request_options,
                "extra_body",
                "additional_body_parameters",
            )
        if len(request_options) == 0:
            return None
        return request_options

    def _convert_tool_calls(
        self, tool_calls: list[ToolCall] | None
    ) -> list[CohereToolCall] | None:
        rtool_calls = []
        if tool_calls is None:
            return None
        for tool_call in tool_calls:
            rtool_calls.append(self._convert_tool_call(tool_call))
        return rtool_calls

    def _convert_tool_call(self, tool_call: ToolCall) -> CohereToolCall:
        return CohereToolCall(
            name=tool_call.function.name,
            parameters=(
                json.loads(tool_call.function.arguments)
                if tool_call.function.arguments is not None
                else {}
            ),
        )

    def _convert_tools(self, tools: list[Tool]) -> list:
        rtools = []
        for tool in tools:
            if tool.type == "function":
                ctool: dict[str, Any] = {}
                ctool["name"] = tool.function.name
                ctool["description"] = tool.function.description
                if (
                    tool.function.parameters is not None
                    and "type" in tool.function.parameters
                    and tool.function.parameters["type"] == "object"
                    and "properties" in tool.function.parameters
                ):
                    params: dict[str, Any] = {}
                    for name, property in tool.function.parameters[
                        "properties"
                    ].items():
                        params[name] = {}
                        params[name]["type"] = property["type"]
                        params[name]["description"] = property["description"]
                        if "enum" in property:
                            params[name]["description"] = (
                                params[name]["description"]
                                + " Possible enum values "
                                + ", ".join(property["enum"])
                                + "."
                            )
                        if "required" in tool.function.parameters:
                            if name in tool.function.parameters["required"]:
                                params[name]["required"] = True
                            else:
                                params[name]["required"] = False
                    ctool["parameter_definitions"] = params
                rtools.append(ctool)
        return rtools
