from abc import ABC, abstractmethod
from pathlib import Path

import fasttext
import spacy
import torch
from couch_potato.core.node import Node
from couch_potato.task.utils import load_targets, save_vector
from gensim.models import Word2Vec as w2v
from huggingface_hub import hf_hub_download
from transformers import BertModel, BertTokenizer


# TODO
# Currently not functional
class ExtractTextFeatures(Node):

    PARAMETERS = {
        "targets": dict | str,
        "separator": str,
        "model_name": str,
        "output_dir": str,
    }

    def __init__(
        self,
        targets: dict | str,
        separator: str,
        model_name: str,
        output_dir: str,
    ) -> None:
        self.targets = targets if isinstance(targets, dict) else load_targets(targets)
        self.separator = "" if separator is None else separator
        self.model = create_model(model_name)
        self.output_dir = Path(output_dir)

    def run(self) -> None:
        for compound, constituents in self.targets.items():
            compound_output_dir = self.output_dir / compound
            compound_output_dir.mkdir(parents=True)

            for target in [
                constituents[0] + self.separator + constituents[1]
            ] + constituents:
                if target == constituents[0] + self.separator + constituents[1]:
                    file_output_path = compound_output_dir / f"{compound}.pt"
                else:
                    file_output_path = compound_output_dir / f"{target}.pt"
                vector = self.model.extract_vector(target)

                save_vector(vector, file_output_path)


class TextToVectorModel(ABC):

    @abstractmethod
    def extract_vector(self, word: str) -> torch.Tensor:
        pass


class FastText(TextToVectorModel):

    def __init__(self) -> None:
        # monkey patch to supress warning
        fasttext.FastText.eprint = lambda x: None

        self.model_path = hf_hub_download(
            repo_id="facebook/fasttext-en-vectors", filename="model.bin"
        )
        self.model = fasttext.load_model(self.model_path)

    def extract_vector(self, word: str) -> torch.Tensor:
        return torch.from_numpy(self.model[word])


class SkipGram(TextToVectorModel):

    def __init__(self) -> None:
        model_path = "TODO"
        self.model = w2v.load(model_path)

    def extract_vector(self, word: str) -> torch.Tensor:
        return torch.tensor(self.model.wv[word])


class Spacy(TextToVectorModel):

    def __init__(self) -> None:
        self.model = spacy.load("en_core_web_lg")

    def extract_vector(self, word: str) -> torch.Tensor:
        return torch.from_numpy(self.model(word).vector)


class Bert(TextToVectorModel):

    def __init__(self) -> None:
        name = "bert-base-uncased"
        self.tokenizer = BertTokenizer.from_pretrained(name)
        self.model = BertModel.from_pretrained(name)
        self.model.eval()

    def extract_vector(self, word: str) -> torch.Tensor:
        input_ids = self.tokenizer.encode(
            word, add_special_tokens=False, return_tensors="pt"
        )

        with torch.no_grad():
            outputs = self.model(input_ids)
            last_hidden_state = outputs.last_hidden_state
            vector = last_hidden_state.squeeze(0)[0]

        return vector


def create_model(model_name: str) -> TextToVectorModel:
    if model_name == "fasttext":
        return FastText()
    elif model_name == "skip-gram"
        return SkipGram()
    elif model_name == "spacy":
        return Spacy()
    elif model_name == "Bert":
        return Bert() 
    else:
        raise ValueError(f"Unknown model name: {model_name}")
