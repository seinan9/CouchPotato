import logging

from couch_potato.core.node import Node
from couch_potato.core.utils import create_dir, join_paths
from couch_potato.task.utils import list_files, load_image, load_targets, save_image
from PIL import Image


class ImagePreprocessor(Node):

    PARAMETERS = {
        "input_dir": str,
        "output_dir": str,
        "targets": dict | str,
        "width": str,
        "height": str,
    }

    def __init__(
        self,
        input_dir: str,
        output_dir: str,
        targets: dict | str,
        width: str,
        height: str,
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.targets = targets if isinstance(targets, dict) else load_targets(targets)
        self.width = width
        self.height = height

    def run(self) -> None:
        progress = 0
        num_targets = len(self.targets)
        for compound in self.targets.keys():
            progress += 1
            self.logger.progress(f"Processing target {progress} out of {num_targets}")

            compound_input_dir = join_paths(self.input_dir, compound)
            compound_output_dir = join_paths(self.output_dir, compound)
            create_dir(compound_output_dir)
            file_names = list_files(compound_input_dir, True)

            for file_name in file_names:
                file_input_path = join_paths(compound_input_dir, file_name)
                file_output_name = f'{file_name.split(".")[0]}.png'
                file_output_path = join_paths(compound_output_dir, file_output_name)

                image = load_image(file_input_path)
                image = image.convert("RGB")
                image = self.resize(image, min(self.width, self.height))
                image = self.crop(image, self.width, self.height)
                save_image(image, file_output_path)

    def resize(self, image: Image, min_size: int) -> Image:
        width, height = image.size
        min_dimension = min(width, height)
        if min_dimension != min_size:
            scale_factor = min_size / min_dimension
            width = int(scale_factor * width)
            height = int(scale_factor * height)
        return image.resize((width, height), Image.Resampling.LANCZOS)

    def crop(self, image: Image, width: int, height: int) -> Image:
        current_width, current_height = image.size
        left = (current_width - width) / 2
        top = (current_height - height) / 2
        right = (current_width + width) / 2
        bottom = (current_height + width) / 2
        return image.crop((left, top, right, bottom))
