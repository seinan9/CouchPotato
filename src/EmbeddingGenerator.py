from abc import ABC, abstractmethod


class EmbeddingGenerator():

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def generate_embedding(self, img_path: str):
        pass
