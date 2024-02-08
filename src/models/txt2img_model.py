from abc import ABC, abstractmethod

class Txt2ImgModel(ABC):

    @abstractmethod
    def generate_image(self, prompt):
        pass
