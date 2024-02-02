from abc import ABC, abstractmethod


class DistanceGenerator(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def generate_distance(self, embedding_0: list[float], embedding_1: list[float]) -> float:
        pass
