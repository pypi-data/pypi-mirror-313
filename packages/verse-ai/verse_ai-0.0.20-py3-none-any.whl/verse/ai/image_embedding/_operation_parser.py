from verse.content.image import Image, ImageParam
from verse.core import OperationParser


class ImageEmbeddingOperationParser(OperationParser):
    def get_image(self) -> Image:
        image = self.get_arg("image")
        return self._normalize_image(image)

    def get_image_as_pil(self):
        image = self.get_image()
        return image.convert("pil")

    def get_images(self) -> list[Image]:
        result = []
        images = self.get_arg("images")
        for image in images:
            result.append(self._normalize_image(image))
        return result

    def get_images_as_pil(self):
        result = []
        images = self.get_arg("images")
        for image in images:
            result.append(self._normalize_image(image).convert("pil"))
        return result

    def _normalize_image(self, image) -> Image:
        if isinstance(image, str):
            return Image(path=image)
        elif isinstance(image, bytes):
            return Image(data=image)
        elif isinstance(image, dict):
            return Image(param=ImageParam.from_dict(image))
        elif isinstance(image, ImageParam):
            return Image(param=image)
        return image

    def get_text(self) -> str:
        return self.get_arg("text")

    def get_texts(self) -> list[str]:
        return self.get_arg("texts")

    def get_embedding1(self) -> list[float]:
        return self.get_arg("embedding1")

    def get_embedding2(self) -> list[float]:
        return self.get_arg("embedding2")
