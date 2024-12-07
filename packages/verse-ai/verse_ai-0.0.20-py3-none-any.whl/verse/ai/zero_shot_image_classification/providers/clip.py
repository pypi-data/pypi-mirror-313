"""
Zero shot image classification using CLIP model.
"""

__all__ = ["Clip"]

from typing import Any

import torch
from transformers import CLIPModel, CLIPProcessor

from verse.core import Context, Operation, Provider, Response

from .._operation import ZeroShotImageClassificationOperation
from .._operation_parser import ZeroShotImageClassificationOperationParser


class Clip(Provider):
    model: str
    device: str | None

    _device: Any
    _model: Any
    _processor: Any

    def __init__(
        self,
        model: str = "openai/clip-vit-base-patch32",
        device: str | None = None,
        **kwargs,
    ):
        """Intialize.

        Args:
            model:
                CLIP model name.
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
        self._model = CLIPModel.from_pretrained(self.model).to(self._device)
        self._processor = CLIPProcessor.from_pretrained(self.model)

    def run(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
        **kwargs,
    ) -> Any:
        self.init(context=context)
        op_parser = ZeroShotImageClassificationOperationParser(operation)
        # CLASSIFY
        if op_parser.op_equals(ZeroShotImageClassificationOperation.CLASSIFY):
            inputs = self._processor(
                images=op_parser.get_image_as_pil(),
                text=op_parser.get_classes(),
                return_tensors="pt",
                padding=True,
            ).to(self._device)
            with torch.no_grad():
                outputs = self._model(**inputs)
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1)
            result = probs.detach().numpy().tolist()[0]
        # BATCH
        elif op_parser.op_equals(ZeroShotImageClassificationOperation.BATCH):
            inputs = self._processor(
                images=op_parser.get_images_as_pil(),
                text=op_parser.get_classes(),
                return_tensors="pt",
                padding=True,
            ).to(self._device)
            with torch.no_grad():
                outputs = self._model(**inputs)
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1)
            result = probs.detach().numpy().tolist()
        else:
            return super().run(
                operation,
                context,
                **kwargs,
            )
        return Response(result=result)
