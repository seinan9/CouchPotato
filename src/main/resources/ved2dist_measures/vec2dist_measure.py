from abc import ABC
from abc import abstractmethod

from torch import Tensor

class Vec2DistMeasure(ABC):

    @abstractmethod
    def calculate(self, vector_0: Tensor, vector_1: Tensor) -> float:
        pass
