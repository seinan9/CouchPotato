from distance_generators.DistanceGenerator import DistanceGenerator
from torch import cosine_similarity

class Cosine(DistanceGenerator):

    def __init__(self):
        pass

    def generate_distance(self, embedding_0: list[float], embedding_1: list[float]) -> float:
        distance = cosine_similarity(embedding_0, embedding_1)
        return distance
