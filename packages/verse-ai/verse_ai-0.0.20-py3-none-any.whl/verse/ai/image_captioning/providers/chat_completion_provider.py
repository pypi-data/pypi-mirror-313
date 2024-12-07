"""
Image captioning using Chat Completion Provider.
"""

__all__ = ["ChatCompletionProvider"]

import json
from typing import Any

from verse.ai.chat_completion._operation import ChatCompletionOperation
from verse.content.image import Image
from verse.core import Component, Context, Operation, Provider, Response

from .._operation import ImageCaptioningOperation
from .._operation_parser import ImageCaptioningOperationParser


class ChatCompletionProvider(Provider):
    component: Component

    def __init__(
        self,
        component: Component,
        **kwargs,
    ):
        """Intialize.

        Args:
            component:
                Chat completion component.
        """
        self.component = component

    def init(self, context: Context | None = None) -> None:
        self.component.init(context=context)

    async def ainit(self, context: Context | None = None) -> None:
        await self.component.ainit(context=context)

    def run(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
        **kwargs,
    ) -> Any:
        self.init(context=context)
        result = None
        op_parser = ImageCaptioningOperationParser(operation)
        noperation, state = self._get_operation(op_parser)
        if noperation is not None:
            nresult = self.component.run(
                noperation,
                context,
                **kwargs,
            )
            result = self._convert_result(op_parser, nresult, state)
            return Response(result=result, native=dict(result=nresult))
        else:
            return super().run(
                operation,
                context,
                **kwargs,
            )

    async def arun(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
        **kwargs,
    ) -> Any:
        await self.ainit(context=context)
        result = None
        op_parser = ImageCaptioningOperationParser(operation)
        noperation, state = self._get_operation(op_parser)
        if noperation is not None:
            nresult = await self.component.arun(
                noperation,
                context,
                **kwargs,
            )
            result = self._convert_result(op_parser, nresult, state)
            return Response(result=result, native=dict(result=result))
        else:
            return super().run(
                operation,
                context,
                **kwargs,
            )

    def _get_operation(
        self, op_parser: ImageCaptioningOperationParser
    ) -> tuple[Operation, dict]:
        state = {}
        converter = OperationConverter()
        # GENERATE
        if op_parser.op_equals(ImageCaptioningOperation.GENERATE):
            state["n"] = 1
            operation = converter.convert_generate(
                op_parser.get_image(), op_parser.get_max_length()
            )
        # BATCH
        elif op_parser.op_equals(ImageCaptioningOperation.BATCH):
            images = op_parser.get_images()
            state["n"] = len(images)
            operation = converter.convert_batch(
                images, op_parser.get_max_length()
            )
        else:
            return None, None
        return operation, state

    def _convert_result(
        self,
        op_parser: ImageCaptioningOperationParser,
        nresult: Any,
        state: dict,
    ) -> Any:
        nresult = nresult.result
        converter = ResultConverter()
        result: Any = None
        # GENERATE
        if op_parser.op_equals(ImageCaptioningOperation.GENERATE):
            result = converter.convert_generate_result(nresult)
        # BATCH
        elif op_parser.op_equals(ImageCaptioningOperation.BATCH):
            n = state["n"]
            result = converter.convert_batch_result(nresult, n)
        return result


class ResultConverter:
    def convert_generate_result(self, nresult: Any) -> str:
        return nresult.choices[0].message.content

    def convert_batch_result(self, result: Any, n: int) -> list[str]:
        json_string = result.choices[0].message.content
        return json.loads(json_string)["captions"]


class OperationConverter:
    def convert_generate(
        self,
        image: Image,
        max_length: int | None = None,
        **kwargs,
    ) -> Operation:
        system_content = "You are an image captioning provider that captions images. For the given image provide a caption in plain text."  # noqa
        if max_length is not None:
            system_content = (
                system_content
                + f" The maximum number of tokens in the caption cannot exceed {max_length}."  # noqa
            )
        messages = [
            {
                "role": "system",
                "content": system_content,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": image,
                    }
                ],
            },
        ]
        return Operation(
            name=ChatCompletionOperation.COMPLETE,
            args={"messages": messages},
        )

    def convert_batch(
        self,
        images: list[Image],
        max_length: int | None = None,
        **kwargs,
    ) -> Operation:
        system_content = """You are an image captioning provider that captions a batch of images. For each image, provide a caption in plain text. One image is not related to another. Return the batch of captions as a JSON object with one array field called 'captions' where each value in the array is the caption of the corresponding image."""  # noqa
        if max_length is not None:
            system_content = (
                system_content
                + f" The maximum number of tokens in the caption cannot exceed {max_length}."  # noqa
            )
        content_parts = []
        for image in images:
            content_parts.append(
                {
                    "type": "image",
                    "image": image,
                }
            )
        messages = [
            {
                "role": "system",
                "content": system_content,
            },
            {"role": "user", "content": content_parts},
        ]
        return Operation(
            name=ChatCompletionOperation.COMPLETE,
            args={
                "messages": messages,
                "response_format": {"type": "json_object"},
            },
        )
