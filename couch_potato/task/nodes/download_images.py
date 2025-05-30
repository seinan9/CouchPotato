from pathlib import Path

from bing_image_downloader import downloader
from couch_potato.core.node import Node
from couch_potato.task.utils import list_files, load_targets, move_file
from tqdm import tqdm


class DownloadImages(Node):
    """
    Node to download images from Bing for a set of target words.

    This node retrieves a specified number of images for each compound and its constituents,
    organizing them by compound in the output directory.

    Parameters:
        - targets: Dictionary (compound -> [constituents] or a YAML file path
        - num_images: Number of images to download per word
        - output_dir: Directory where images are saved
    """

    PARAMETERS = {"targets": dict | str, "num_images": int, "output_dir": str}

    def __init__(
        self,
        targets: dict | str,
        num_images: int,
        output_dir: str,
    ) -> None:
        self.targets = targets if isinstance(targets, dict) else load_targets(targets)
        self.num_images = num_images
        self.output_dir = Path(output_dir)

    def run(self) -> None:
        tmp_dir = self.output_dir / "tmp"  # Temporary directory for raw downloads

        for compound, constituents in tqdm(
            self.targets.items(), desc="Downloading images for targets"
        ):
            words = [compound] + constituents

            # Download images for each word into the temp directory
            for word in words:
                downloader.download(
                    query=word,
                    limit=self.num_images,
                    output_dir=tmp_dir,
                    adult_filter_off=True,
                    force_replace=False,
                    timeout=3,
                    verbose=False,
                    filter="photo",
                )

            # Create a directory for the current compound
            compound_output_dir = self.output_dir / compound
            compound_output_dir.mkdir(parents=True)

            # Move and rename each downloaded image into the compound's directory
            for word in words:
                word_dir = tmp_dir / word
                files = list_files(word_dir, True)

                for file in files:
                    file_number = file.split("_")[1].split(".")[0]
                    file_extension = file.split(".")[1]
                    file_input_path = word_dir / file
                    file_output_path = (
                        compound_output_dir / f"{word}_{file_number}.{file_extension}"
                    )
                    move_file(file_input_path, file_output_path)

                # Clean up temporary word directory
                word_dir.rmdir()

        # Clean up the overall temp directory
        tmp_dir.rmdir()
