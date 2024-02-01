from abc import ABC, abstractmethod

class ImageGenerator(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def generate_image(self, prompt: list[str]) -> list:
        pass