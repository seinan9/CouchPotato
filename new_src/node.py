from abc import ABC
from abc import abstractmethod

class Node(ABC):

    def __init__(self, input_dir: str, output_dir: str) -> None:
        print(f'Initializing {self.__class__.__name__}')
        self.input_dir = input_dir
        self.output_dir = output_dir

    def run(self) -> None:
        print(f'Executing {self.__class__.__name__}')
