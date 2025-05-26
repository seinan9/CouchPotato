from abc import ABC, abstractmethod


class Node(ABC):
    PARAMETERS = {}

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass
