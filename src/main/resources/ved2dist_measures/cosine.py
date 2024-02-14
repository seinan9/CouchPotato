import torch

from resources.ved2dist_measures.vec2dist_measure import Vec2DistMeasure


class Cosine(Vec2DistMeasure):

    def __init__(self):
        pass

    def calculate(self, vector_0: torch.Tensor, vector_1: torch.Tensor) -> float:
        return torch.cosine_similarity(vector_0, vector_1, dim=0).numpy().tolist()
