"""
Image captioning using BLIP model.
"""

__all__ = ["Blip"]

from typing import Any

import torch
from transformers import BlipForConditionalGeneration, BlipProcessor

from verse.core import Context, Operation, Provider, Response

from .._operation import ImageCaptioningOperation
from .._operation_parser import ImageCaptioningOperationParser


class Blip(Provider):
    model: str
    device: str | None

    _device: Any
    _model: Any
    _processor: Any

    def __init__(
        self,
        model: str = "Salesforce/blip-image-captioning-base",
        device: str | None = None,
        **kwargs,
    ):
        """Intialize.

        Args:
            model:
                BLIP model name.
            device:
                Pytorch device name.
        """
        self.model = model
        self.device = device

        self._model = None
        self._device = None
        self._processor = None

    def init(self, context: Context | None = None) -> None:
        if self._model:
            return
        self._device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        if self.device is not None:
            self._device = self.device
        self._model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        ).to(self._device)
        self._processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

    def run(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
        **kwargs,
    ) -> Any:
        self.init(context=context)
        op_parser = ImageCaptioningOperationParser(operation)
        # GENERATE
        if op_parser.op_equals(ImageCaptioningOperation.GENERATE):
            inputs = self._processor(
                op_parser.get_image_as_pil(),
                return_tensors="pt",
            ).to(self._device)
            max_length = op_parser.get_max_length()
            with torch.no_grad():
                if max_length:
                    outputs = self._model.generate(
                        **inputs, max_length=max_length
                    )
                else:
                    outputs = self._model.generate(**inputs)
            caption = self._processor.decode(
                outputs[0], skip_special_tokens=True
            )
            result = caption
        # BATCH
        elif op_parser.op_equals(ImageCaptioningOperation.BATCH):
            inputs = self._processor(
                op_parser.get_images_as_pil(),
                return_tensors="pt",
            ).to(self._device)
            max_length = op_parser.get_max_length()
            with torch.no_grad():
                if max_length:
                    outputs = self._model.generate(
                        **inputs, max_length=max_length
                    )
                else:
                    outputs = self._model.generate(**inputs)
            captions = [
                self._processor.decode(output, skip_special_tokens=True)
                for output in outputs
            ]
            result = captions
        else:
            return super().run(
                operation,
                context,
                **kwargs,
            )
        return Response(result=result)
