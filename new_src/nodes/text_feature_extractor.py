import fasttext
import torch

from abc import ABC
from abc import abstractmethod
from huggingface_hub import hf_hub_download

from node import Node
from helpers.storage_helper import StorageHelper
from utils import Utils


class TextFeatureExtractor(Node):

    PARAMETERS = {
        'output_dir': str,
        'targets': dict | str,
        'model_id': str
    }

    def __init__(self, output_dir: str, targets: dict | str, model_id: str) -> None:
        self.output_dir = output_dir
        self.targets = targets if isinstance(
            targets, dict) else StorageHelper.load_targets(targets)
        self.model: TextToVectorModel = globals()[model_id]()

    def run(self) -> None:
        for compound, constituents in self.targets.items():
            compound_output_dir = Utils.join_paths(self.output_dir, compound)
            Utils.create_dir(compound_output_dir)

            for target in [compound] + constituents:
                file_output_path = Utils.join_paths(
                    compound_output_dir, f'{target}_0.pt')
                vector = self.model.extract_vector(target)
                StorageHelper.save_vector(vector, file_output_path)


class TextToVectorModel(ABC):

    @abstractmethod
    def extract_vector(self, word: str) -> torch.Tensor:
        pass


class FastText(TextToVectorModel):

    def __init__(self) -> None:
        # monkey patch to supress warning
        fasttext.FastText.eprint = lambda x: None

        self.model_path = hf_hub_download(
            repo_id="facebook/fasttext-en-vectors", filename="model.bin")
        self.model = fasttext.load_model(self.model_path)

    def extract_vector(self, word: str) -> torch.Tensor:
        return torch.from_numpy(self.model[word])
