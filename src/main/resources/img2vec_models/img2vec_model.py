from abc import ABC
from abc import abstractmethod

import torch
from PIL import Image

class Img2VecModel(ABC):

    @abstractmethod
    def create_vector(self, image: Image.Image) -> torch.Tensor:
        pass