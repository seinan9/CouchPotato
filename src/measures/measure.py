from abc import ABC, abstractmethod

class Measure(ABC):

    @abstractmethod
    def calculate_measure(vec_0, vec_1):
        pass
