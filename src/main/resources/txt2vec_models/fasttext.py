import fasttext
import torch

from huggingface_hub import hf_hub_download

from resources.txt2vec_models.txt2vec_model import Txt2VecModel

class FastText(Txt2VecModel):

    def __init__(self):
        self.model_path = hf_hub_download(repo_id="facebook/fasttext-en-vectors", filename="model.bin")
        self.model = fasttext.load_model(self.model_path)

    def create_vector(self, word: str) -> torch.Tensor:
        return torch.from_numpy(self.model[word])
    