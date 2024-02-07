from abc import ABC, abstractmethod

class Word2ImgModel(ABC):

    @abstractmethod
    def generate_image(self, prompt):
        pass
