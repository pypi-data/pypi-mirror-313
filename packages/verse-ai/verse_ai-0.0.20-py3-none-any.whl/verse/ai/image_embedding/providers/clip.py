"""
Image embedding using CLIP model.
"""

__all__ = ["Clip"]

from typing import Any

import torch
from transformers import CLIPModel, CLIPProcessor

from verse.core import Context, Operation, Provider, Response

from .._operation import ImageEmbeddingOperation
from .._operation_parser import ImageEmbeddingOperationParser


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
        op_parser = ImageEmbeddingOperationParser(operation)
        # EMBED IMAGE
        if op_parser.op_equals(ImageEmbeddingOperation.EMBED):
            inputs = self._processor(
                images=op_parser.get_image_as_pil(),
                return_tensors="pt",
                padding=True,
            ).to(self._device)
            with torch.no_grad():
                embeddings = self._model.get_image_features(**inputs)
            embeddings = embeddings / embeddings.norm(dim=-1, keepdim=True)
            result = embeddings.cpu().numpy().flatten().tolist()
        # BATCH EMBED IMAGE
        elif op_parser.op_equals(ImageEmbeddingOperation.BATCH):
            inputs = self._processor(
                images=op_parser.get_images_as_pil(),
                return_tensors="pt",
                padding=True,
            ).to(self._device)
            with torch.no_grad():
                embeddings = self._model.get_image_features(**inputs)
            embeddings = embeddings / embeddings.norm(dim=-1, keepdim=True)
            result = [
                embedding.cpu().numpy().flatten().tolist()
                for embedding in embeddings
            ]
        # EMBED TEXT
        elif op_parser.op_equals(ImageEmbeddingOperation.EMBED_TEXT):
            inputs = self._processor(
                text=op_parser.get_text(),
                return_tensors="pt",
                padding=True,
            ).to(self._device)
            with torch.no_grad():
                embeddings = self._model.get_text_features(**inputs)
            embeddings = embeddings / embeddings.norm(dim=-1, keepdim=True)
            result = embeddings.cpu().numpy().flatten().tolist()
        # BATCH EMBED TEXT
        elif op_parser.op_equals(ImageEmbeddingOperation.BATCH_TEXT):
            inputs = self._processor(
                text=op_parser.get_texts(),
                return_tensors="pt",
                padding=True,
            ).to(self._device)
            with torch.no_grad():
                embeddings = self._model.get_text_features(**inputs)
            embeddings = embeddings / embeddings.norm(dim=-1, keepdim=True)
            result = [
                embedding.cpu().numpy().flatten().tolist()
                for embedding in embeddings
            ]
        # BATCH EMBED IMAGE TEXT
        elif op_parser.op_equals(ImageEmbeddingOperation.BATCH_IMAGE_TEXT):
            inputs = self._processor(
                text=op_parser.get_texts(),
                images=op_parser.get_images_as_pil(),
                return_tensors="pt",
                padding=True,
            ).to(self._device)
            with torch.no_grad():
                image_embeddings = self._model.get_image_features(
                    pixel_values=inputs["pixel_values"]
                )
                text_embeddings = self._model.get_text_features(
                    input_ids=inputs["input_ids"],
                    attention_mask=inputs["attention_mask"],
                )
            image_embeddings = image_embeddings / image_embeddings.norm(
                dim=-1, keepdim=True
            )
            text_embeddings = text_embeddings / text_embeddings.norm(
                dim=-1, keepdim=True
            )
            result = (
                [
                    embedding.cpu().numpy().flatten().tolist()
                    for embedding in image_embeddings
                ],
                [
                    embedding.cpu().numpy().flatten().tolist()
                    for embedding in text_embeddings
                ],
            )
        # COMPARE
        elif op_parser.op_equals(ImageEmbeddingOperation.COMPARE):
            embedding1 = torch.tensor(op_parser.get_embedding1())
            embedding2 = torch.tensor(op_parser.get_embedding2())
            similarity = torch.nn.functional.cosine_similarity(
                embedding1, embedding2, dim=0
            )
            result = similarity.item()
        else:
            return super().run(operation, context, **kwargs)
        return Response(result=result)
