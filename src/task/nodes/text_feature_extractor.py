import fasttext
import torch

from abc import ABC
from abc import abstractmethod
from gensim.models import Word2Vec as w2v
from huggingface_hub import hf_hub_download

from core.node import Node
from core.utils import create_dir, join_paths
from task.utils import load_targets, save_vector


class TextFeatureExtractor(Node):

    PARAMETERS = {
        'output_dir': str,
        'targets': dict | str,
        'model_id': str,
        'model_path': str
    }

    def __init__(self, output_dir: str, targets: dict | str, model_id: str, model_path: str = None) -> None:
        self.output_dir = output_dir
        self.targets = targets if isinstance(
            targets, dict) else load_targets(targets)
        self.model: TextToVectorModel = globals()[model_id](model_path)

    def run(self) -> None:
        for compound, constituents in self.targets.items():
            compound_output_dir = join_paths(self.output_dir, compound)
            create_dir(compound_output_dir)

            for target in [constituents[0] + "_" + constituents[1]] + constituents:
                if target == constituents[0] + "_" + constituents[1]:
                    file_output_path = join_paths(
                        compound_output_dir, f'{compound}.pt'
                    )
                else:
                    file_output_path = join_paths(
                        compound_output_dir, f'{target}.pt')
                vector = self.model.extract_vector(target)

                save_vector(vector, file_output_path)


class TextToVectorModel(ABC):

    @abstractmethod
    def extract_vector(self, word: str) -> torch.Tensor:
        pass


class FastText(TextToVectorModel):

    def __init__(self, model_path) -> None:
        # monkey patch to supress warning
        fasttext.FastText.eprint = lambda x: None

        self.model_path = hf_hub_download(
            repo_id="facebook/fasttext-en-vectors", filename="model.bin")
        self.model = fasttext.load_model(self.model_path)

    def extract_vector(self, word: str) -> torch.Tensor:
        return torch.from_numpy(self.model[word])


class Word2Vec(TextToVectorModel):

    def __init__(self, model_path) -> None:
        self.model = w2v.load(model_path)

    def extract_vector(self, word: str) -> torch.Tensor:
        return torch.tensor(self.model.wv[word])
