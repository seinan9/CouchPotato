from abc import ABC
from abc import abstractmethod

from PIL.Image import Image
from torch import Tensor

class Img2VecModel(ABC):

    @abstractmethod
    def create_vector(self, image: Image) -> Tensor:
        pass