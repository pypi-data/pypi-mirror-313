from typing import Any

from verse.content.image import Image, ImageParam
from verse.core import Component, Response

from ._operation import ImageEmbeddingOperation


class ImageEmbedding(Component):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def embed(
        self,
        image: str | bytes | Image | ImageParam | dict,
        **kwargs: Any,
    ) -> Response[list[float]]:
        """Create embedding for image.

        Args:
            image: Image.

        Returns:
            Image embedding.
        """
        return self._run_internal(ImageEmbeddingOperation.EMBED, locals())

    def compare(
        self,
        embedding1: list[float],
        embedding2: list[float],
        **kwargs,
    ) -> Response[float]:
        """Compare embeddings using cosine similarity.

        Args:
            embedding1: Embedding 1.
            embedding2: Embedding 2.

        Returns:
            Similarity score.
        """
        return self._run_internal(ImageEmbeddingOperation.COMPARE, locals())

    def batch(
        self,
        images: list[str | bytes | Image | ImageParam | dict],
        **kwargs: Any,
    ) -> Response[list[list[float]]]:
        """Create embedding for batch of images.

        Args:
            images: List of images.

        Returns:
            List of image embeddings.
        """
        return self._run_internal(ImageEmbeddingOperation.BATCH, locals())

    def embed_text(
        self,
        text: str,
        **kwargs: Any,
    ) -> Response[list[float]]:
        """Create embedding for text.

        Args:
            text: Text string.

        Returns:
            Text embedding.
        """
        return self._run_internal(ImageEmbeddingOperation.EMBED_TEXT, locals())

    def batch_text(
        self,
        texts: list[str],
        **kwargs: Any,
    ) -> Response[list[list[float]]]:
        """Create embedding for batch of text.

        Args:
            texts: List of texts.

        Returns:
            List of text embeddings.
        """
        return self._run_internal(ImageEmbeddingOperation.BATCH_TEXT, locals())

    def batch_image_text(
        self,
        images: list[str | bytes | Image | ImageParam | dict],
        texts: list[str],
        **kwargs: Any,
    ) -> Response[tuple[list[list[float]], list[list[float]]]]:
        """Create embedding for batch of images and texts.

        Args:
            images: List of images.
            texts: List of texts.

        Returns:
            Tuple of list of image embeddings and text embeddings.
        """
        return self._run_internal(
            ImageEmbeddingOperation.BATCH_IMAGE_TEXT, locals()
        )

    async def aembed(
        self,
        image: Image | ImageParam | dict,
        **kwargs: Any,
    ) -> Response[list[float]]:
        """Create embedding for image.

        Args:
            image: Image.

        Returns:
            Image embedding.
        """
        return await self._arun_internal(
            ImageEmbeddingOperation.EMBED, locals()
        )

    async def acompare(
        self,
        embedding1: list[float],
        embedding2: list[float],
        **kwargs,
    ) -> Response[float]:
        """Compare embeddings using cosine similarity.

        Args:
            embedding1: Embedding 1.
            embedding2: Embedding 2.

        Returns:
            Similarity score.
        """
        return await self._arun_internal(
            ImageEmbeddingOperation.COMPARE, locals()
        )

    async def abatch(
        self,
        images: list[Image | ImageParam | dict],
        **kwargs: Any,
    ) -> Response[list[list[float]]]:
        """Create embedding for batch of images.

        Args:
            images: List of images.

        Returns:
            List of image embeddings.
        """
        return await self._arun_internal(
            ImageEmbeddingOperation.BATCH, locals()
        )

    async def aembed_text(
        self,
        text: str,
        **kwargs: Any,
    ) -> Response[list[float]]:
        """Create embedding for text.

        Args:
            text: Text string.

        Returns:
            Text embedding.
        """
        return await self._arun_internal(
            ImageEmbeddingOperation.EMBED_TEXT, locals()
        )

    async def abatch_text(
        self,
        texts: list[str],
        **kwargs: Any,
    ) -> Response[list[list[float]]]:
        """Create embedding for batch of text.

        Args:
            texts: List of texts.

        Returns:
            List of text embeddings.
        """
        return await self._arun_internal(
            ImageEmbeddingOperation.BATCH_TEXT, locals()
        )

    async def abatch_image_text(
        self,
        images: list[Image | ImageParam | dict],
        texts: list[str],
        **kwargs: Any,
    ) -> Response[tuple[list[list[float]], list[list[float]]]]:
        """Create embedding for batch of images and texts.

        Args:
            images: List of images.
            texts: List of texts.

        Returns:
            Tuple of list of image embeddings and text embeddings.
        """
        return await self._arun_internal(
            ImageEmbeddingOperation.BATCH_IMAGE_TEXT, locals()
        )
