from typing import Any

from verse.content.image import Image, ImageParam
from verse.core import Component, Response

from ._operation import ImageCaptioningOperation


class ImageCaptioning(Component):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def generate(
        self,
        image: str | bytes | Image | ImageParam | dict,
        max_length: int | None = None,
        **kwargs: Any,
    ) -> Response[str]:
        """Generate caption for image.

        Args:
            image: Image.

        Returns:
            Caption.
        """
        return self._run_internal(ImageCaptioningOperation.GENERATE, locals())

    def batch(
        self,
        images: list[str | bytes | Image | ImageParam | dict],
        max_length: int | None = None,
        **kwargs: Any,
    ) -> Response[list[str]]:
        """Generate captions for batch of images.

        Args:
            images: List of images.

        Returns:
            List of captions.
        """
        return self._run_internal(ImageCaptioningOperation.BATCH, locals())

    async def agenerate(
        self,
        image: str | bytes | Image | ImageParam | dict,
        **kwargs: Any,
    ) -> Response[str]:
        """Generate caption for image.

        Args:
            image: Image.

        Returns:
            Caption.
        """
        return await self._arun_internal(
            ImageCaptioningOperation.GENERATE, locals()
        )

    async def abatch(
        self,
        images: list[str | bytes | Image | ImageParam | dict],
        **kwargs: Any,
    ) -> Response[list[str]]:
        """Generate captions for batch of images.

        Args:
            images: List of images.

        Returns:
            List of captions.
        """
        return await self._arun_internal(
            ImageCaptioningOperation.BATCH, locals()
        )
