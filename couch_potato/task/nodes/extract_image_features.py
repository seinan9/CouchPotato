from abc import ABC, abstractmethod
from pathlib import Path

import torch
import torchvision
from couch_potato.core.node import Node
from couch_potato.task.utils import list_files, load_image, load_targets, save_vector
from PIL.Image import Image
from tqdm import tqdm


class ExtractImageFeatures(Node):
    """
    Node to extract feature vectors from images using a specified deep vision model.

    This node processes images organized by compound names and extracts vector representations
    using a model such as a Vision Transformer (ViT). Outputs are saved as PyTorch tensor files.

    Parameters:
        - input_dir: Directory containing folders named after compounds, with images inside.
        - targets: Dictionary or YAML path mapping compounds to their constituents.
        - model_name: String identifier for the image model to use (e.g., "vit").
        - cuda_id: GPU device ID to use for inference.
        - output_dir: Directory where extracted vectors will be saved.
    """

    PARAMETERS = {
        "input_dir": str,
        "targets": dict,
        "model_name": str,
        "cuda_id": int,
        "output_dir": str,
    }

    def __init__(
        self,
        input_dir: str,
        model_name: str,
        targets: dict | str,
        cuda_id: int,
        output_dir: str,
    ) -> None:
        self.input_dir = Path(input_dir)
        self.targets = targets if isinstance(targets, dict) else load_targets(targets)
        self.model = create_model(model_name, cuda_id)
        self.output_dir = Path(output_dir)

    def run(self) -> None:
        # Iterate over each compound and extract features from the images in its subdirectory (this contains images for the compound and the constituents)
        for compound in tqdm(
            self.targets.keys(), desc="Extracting features for targets"
        ):

            compound_input_dir = self.input_dir / compound
            compound_output_dir = self.output_dir / compound
            compound_output_dir.mkdir(parents=True)

            file_names = list_files(compound_input_dir, False)
            for file_name in file_names:
                file_input_path = compound_input_dir / f"{file_name}.png"
                file_output_path = compound_output_dir / f"{file_name}.pt"

                image = load_image(file_input_path)
                vector = self.model.extract_vector(image)
                save_vector(vector, file_output_path)


class ImageToVectorModel(ABC):

    @abstractmethod
    def extract_vector(self, image: Image) -> torch.Tensor:
        pass


class VisionTransformer(ImageToVectorModel):

    def __init__(self, cuda_id: int) -> None:
        self.device = torch.device(f"cuda:{cuda_id}")
        self.model = torchvision.models.vit_h_14(
            weights=torchvision.models.ViT_H_14_Weights.DEFAULT
        )

        # Remove the classification head to get pure feature vectors
        self.model.heads = torch.nn.Sequential(*list(self.model.heads.children())[:-1])
        self.model.to(self.device)
        self.model.eval()  # TODO: Check whether this makes a difference

        # Standard ImageNet preprocessing and resizing
        self.transform = torchvision.transforms.Compose(
            [
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize(
                    (0.485, 0.456, 0.406), (0.229, 0.224, 0.225)
                ),
                torchvision.transforms.Resize((518, 518)),
            ]
        )

    def extract_vector(self, image: Image) -> torch.Tensor:
        # Preprocess, move to GPU, run through model, detach and move to CPU
        image = self.transform(image).float().unsqueeze_(0).to(self.device)
        with torch.no_grad():
            return self.model(image).squeeze(0).cpu()


def create_model(model_name: str, cuda_id: str) -> ImageToVectorModel:
    if model_name == "vit":
        return VisionTransformer(cuda_id)
    else:
        raise ValueError(f"Unknown model name: {model_name}")
