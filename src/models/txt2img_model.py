from abc import ABC
from abc import abstractmethod

from PIL.Image import Image

class Txt2ImgModel(ABC):

    @abstractmethod
    def generate_image(self, prompt: list[str]) -> list[Image]:
        pass
