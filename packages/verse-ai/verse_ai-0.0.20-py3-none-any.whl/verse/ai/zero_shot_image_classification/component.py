from typing import Any

from verse.content.image import Image, ImageParam
from verse.core import Component, Response

from ._operation import ZeroShotImageClassificationOperation


class ZeroShotImageClassification(Component):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def classify(
        self,
        image: str | bytes | Image | ImageParam | dict,
        classes: list[str],
        **kwargs: Any,
    ) -> Response[list[float]]:
        """Zero-shot classification of image with provided texts.

        Args:
            image: Image to classify.
            texts: List of classes as texts.

        Returns:
            Classification results.
        """
        return self._run_internal(
            ZeroShotImageClassificationOperation.CLASSIFY, locals()
        )

    def batch(
        self,
        images: list[str | bytes | Image | ImageParam | dict],
        classes: list[str],
        **kwargs: Any,
    ) -> Response[list[list[float]]]:
        """Zero-shot classification of images with provided texts.

        Args:
            images: Images to classify.
            texts: List of classes as texts.

        Returns:
            List of classification results.
        """
        return self._run_internal(
            ZeroShotImageClassificationOperation.BATCH, locals()
        )

    async def aclassify(
        self,
        image: Image,
        classes: list[str],
        **kwargs: Any,
    ) -> Response[list[float]]:
        """Zero-shot classification of image with provided texts.

        Args:
            image: Image to classify.
            texts: List of classes as texts.

        Returns:
            Classification results.
        """
        return await self._arun_internal(
            ZeroShotImageClassificationOperation.CLASSIFY, locals()
        )

    async def abatch(
        self,
        images: list[Image],
        classes: list[str],
        **kwargs: Any,
    ) -> Response[list[list[float]]]:
        """Zero-shot classification of images with provided texts.

        Args:
            images: Images to classify.
            texts: List of classes as texts.

        Returns:
            List of classification results.
        """
        return await self._arun_internal(
            ZeroShotImageClassificationOperation.BATCH, locals()
        )
