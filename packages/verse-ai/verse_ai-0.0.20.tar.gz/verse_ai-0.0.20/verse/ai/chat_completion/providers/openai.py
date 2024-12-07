from __future__ import annotations

__all__ = ["OpenAI"]

from typing import Any

from verse.content.image import Image, ImageParam
from verse.core import Context, NCall, Operation, Provider, Response
from verse.core.exceptions import BadRequestError

from .._helper import copy_arg
from .._models import ChatCompletionResult, Stream
from .._operation import ChatCompletionOperation
from .._operation_parser import ChatCompletionOperationParser


class OpenAI(Provider):
    model: str | None
    api_key: str | None
    organization: str | None
    project: str | None
    base_url: str | None
    timeout: float | None
    service_tier: str | None
    nparams: dict

    _client: Any
    _aclient: Any

    def __init__(
        self,
        model: str | None = "gpt-4o",
        api_key: str | None = None,
        organization: str | None = None,
        project: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
        service_tier: str | None = None,
        nparams: dict = dict(),
    ):
        """Initialize.

        Args:
            model:
                OpenAI model to use for chat completion.
            api_key:
                OpenAI API key.
            organization:
                OpenAI organization.
            project:
                OpenAI project.
            base_url:
                OpenAI base url.
            timeout:
                Timeout for client.
            service_tier:
                OpenAI service tier.
            nparams:
                Native params for OpenAI client.
        """
        self.model = model
        self.api_key = api_key
        self.organization = organization
        self.project = project
        self.base_url = base_url
        self.timeout = timeout
        self.service_tier = service_tier
        self.nparams = nparams

        self._client = None
        self._aclient = None

    def init(self, context: Context | None = None) -> None:
        if self._client is not None:
            return

        from openai import OpenAI

        self._client = OpenAI(**self._get_client_params())

    async def ainit(self, context: Context | None = None) -> None:
        if self._aclient is not None:
            return

        from openai import AsyncOpenAI

        self._aclient = AsyncOpenAI(**self._get_client_params())

    def _get_client_params(self) -> dict[str, Any]:
        args: dict = {}
        if self.api_key is not None:
            args["api_key"] = self.api_key
        if self.organization is not None:
            args["organization"] = self.organization
        if self.project is not None:
            args["project"] = self.project
        if self.base_url is not None:
            args["base_url"] = self.base_url
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
        )
        if ncall is None:
            return super().run(
                operation=operation,
                context=context,
                **kwargs,
            )
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
        )
        if ncall is None:
            return await super().arun(
                operation=operation,
                context=context,
                **kwargs,
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
    ) -> tuple[NCall | None, dict]:
        call = None
        state: dict = {}
        nargs = op_parser.get_nargs()
        op_converter = OperationConverter(self.model, self.service_tier)
        # COMPLETE
        if op_parser.op_equals(ChatCompletionOperation.COMPLETE):
            args = op_converter.convert_complete(op_parser.get_args())
            call = NCall(
                client.chat.completions.create,
                args,
                nargs,
            )
        # STREAM
        elif op_parser.op_equals(ChatCompletionOperation.STREAM):
            args = op_converter.convert_stream(op_parser.get_args())
            call = NCall(
                client.chat.completions.create,
                args,
                nargs,
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
            )
        # STREAM
        if op_parser.op_equals(ChatCompletionOperation.STREAM):
            result = result_converter.convert_stream_result(
                nresult,
            )
        return result


class ResultConverter:
    def __init__(self):
        pass

    def convert_complete_result(
        self,
        nresult: Any,
    ) -> ChatCompletionResult:
        return ChatCompletionResult.model_validate(nresult.model_dump())

    def convert_stream_result(
        self,
        nresult: Any,
    ) -> Stream:
        return Stream(nresult, self.convert_complete_result)


class OperationConverter:
    model: str | None
    service_tier: str | None

    def __init__(self, model: str | None, service_tier: str | None):
        self.model = model
        self.service_tier = service_tier

    def convert_complete(
        self,
        args: dict,
    ) -> dict:
        return self._convert_args(args)

    def convert_stream(
        self,
        args: dict,
    ) -> dict:
        rargs = self._convert_args(args)
        rargs["stream"] = True
        return rargs

    def _convert_messages(self, messages: list):
        for message in messages:
            content = message["content"]
            if isinstance(content, list):
                for part in content:
                    if part["type"] == "image":
                        image_part = part["image"]
                        if isinstance(image_part, Image):
                            image = image_part
                        elif isinstance(image_part, ImageParam):
                            image = Image(param=image_part)
                        elif isinstance(image_part, dict):
                            image = Image(
                                param=ImageParam.from_dict(image_part)
                            )
                        else:
                            raise BadRequestError("Image content not valid.")
                        if image.url is not None:
                            part["image_url"] = {"url": image.url}
                        else:
                            base64 = image.convert(
                                type="base64", format="jpeg"
                            )
                            part["image_url"] = {
                                "url": f"data:image/jpeg;base64,{base64}"
                            }
                        part.pop("image")
                        part["type"] = "image_url"

    def _convert_args(self, args: dict) -> dict:
        rargs: dict = {}
        if "model" not in args:
            rargs["model"] = self.model
        else:
            copy_arg(args, rargs, "model")
        if self.service_tier is not None:
            args["service_tier"] = self.service_tier
        copy_arg(args, rargs, "messages")
        self._convert_messages(rargs["messages"])
        copy_arg(args, rargs, "temperature")
        copy_arg(args, rargs, "top_p")
        copy_arg(args, rargs, "max_tokens")
        copy_arg(args, rargs, "stop")
        copy_arg(args, rargs, "n")
        copy_arg(args, rargs, "presence_penalty")
        copy_arg(args, rargs, "frequency_penalty")
        copy_arg(args, rargs, "tools")
        copy_arg(args, rargs, "tool_choice")
        copy_arg(args, rargs, "parallel_tool_calls")
        copy_arg(args, rargs, "response_format")
        copy_arg(args, rargs, "seed")
        copy_arg(args, rargs, "logit_bias")
        copy_arg(args, rargs, "logprobs")
        copy_arg(args, rargs, "stream_options")
        copy_arg(args, rargs, "top_logprobs")
        copy_arg(args, rargs, "user")
        copy_arg(args, rargs, "extra_headers")
        copy_arg(args, rargs, "extra_query")
        copy_arg(args, rargs, "extra_body")
        copy_arg(args, rargs, "timeout")
        return rargs
