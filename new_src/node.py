from abc import ABC
from abc import abstractmethod


class Node(ABC):

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass
