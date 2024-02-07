from abc import ABC, abstractmethod

class Img2VecModel(ABC):

    @abstractmethod
    def generate_embedding(self, img_file):
        pass