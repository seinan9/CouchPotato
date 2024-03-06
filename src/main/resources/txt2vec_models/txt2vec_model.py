import torch

from abc import ABC
from abc import abstractmethod

class Txt2VecModel(ABC):

    @abstractmethod
    def create_vector(self, word: str) -> torch.Tensor:
        pass

