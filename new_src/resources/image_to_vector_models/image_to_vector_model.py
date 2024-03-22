import torch

from abc import ABC
from abc import abstractmethod
from PIL.Image import Image

class ImageToVectorModel(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def extract_vector(self, image: Image) -> torch.Tensor:
        pass
