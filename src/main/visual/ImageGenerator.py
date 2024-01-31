from abc import ABC, abstractmethod

class ImageGenerator:

    @abstractmethod
    def __ini__(self):
        pass

    @abstractmethod
    def generate_image(self, prompt: list[str]) -> list:
        pass