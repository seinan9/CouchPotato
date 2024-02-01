import torch


class Similarity():
    def __init__(self):
        pass

    def get_cosine_similarity(self, emb_1, emb_2):
        scores = torch.nn.functional.cosine_similarity(emb_1, emb_2)

        return scores.numpy().tolist()
