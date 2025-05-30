from pathlib import Path

from couch_potato.core.node import Node
from couch_potato.task.utils import list_files, load_image, load_targets, save_image
from PIL import Image
from tqdm import tqdm


class PreprocessImages(Node):
    """
    Node for preprocessing images by resizing and cropping.

    Parameters:
        - input_dir: Directory with original images.
        - targets: Dictionary or YAML path mapping compounds to their constituents.
        - width: Desired width after cropping.
        - height: Desired height after cropping.
        - output_dir: Directory to store preprocessed images.
    """

    PARAMETERS = {
        "input_dir": str,
        "targets": dict | str,
        "width": int,
        "height": int,
        "output_dir": str,
    }

    def __init__(
        self,
        input_dir: str,
        targets: dict | str,
        width: int,
        height: int,
        output_dir: str,
    ) -> None:
        self.input_dir = Path(input_dir)
        self.targets = targets if isinstance(targets, dict) else load_targets(targets)
        self.width = width
        self.height = height
        self.output_dir = Path(output_dir)

    def run(self) -> None:
        # Loop over each compound and process its images
        for compound in tqdm(self.targets.keys(), desc="Preprocessing images"):
            compound_input_dir = self.input_dir / compound
            compound_output_dir = self.output_dir / compound
            compound_output_dir.mkdir(parents=True)
            file_names = list_files(compound_input_dir, True)

            for file_name in file_names:
                file_input_path = compound_input_dir / file_name
                file_output_path = (
                    compound_output_dir / f"{file_name.split('.')[0]}.png"
                )

                image = load_image(file_input_path)
                image = image.convert("RGB")
                image = self.resize(image, min(self.width, self.height))
                image = self.crop(image, self.width, self.height)
                save_image(image, file_output_path)

    def resize(self, image: Image, min_size: int) -> Image:
        """
        Resize images such that the smaller dimension equals 'min_size', maintaining aspect ratio
        """
        width, height = image.size
        min_dimension = min(width, height)
        if min_dimension != min_size:
            scale_factor = min_size / min_dimension
            width = int(scale_factor * width)
            height = int(scale_factor * height)
        return image.resize((width, height), Image.Resampling.LANCZOS)

    def crop(self, image: Image, width: int, height: int) -> Image:
        """
        Center crop image to the given with and height
        """
        current_width, current_height = image.size
        left = (current_width - width) / 2
        top = (current_height - height) / 2
        right = (current_width + width) / 2
        bottom = (current_height + width) / 2
        return image.crop((left, top, right, bottom))
