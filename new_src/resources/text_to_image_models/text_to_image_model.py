from abc import ABC
from abc import abstractmethod
from PIL.Image import Image

class TextToImageModel(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def generate_image(self, seed: int, prompt: str, steps: int, cfg: float) -> Image:
        pass
