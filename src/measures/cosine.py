from torch import cosine_similarity
from measures.measure import Measure


class Cosine(Measure):

    def __init__(self):
        pass

    def calculate_measure(self, vec_0, vec_1):
        return cosine_similarity(vec_0, vec_1).numpy().tolist()
