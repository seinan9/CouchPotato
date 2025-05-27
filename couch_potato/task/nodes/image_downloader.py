import logging

from bing_image_downloader import downloader
from couch_potato.core.node import Node
from couch_potato.core.utils import create_dir, join_paths, remove_dir
from couch_potato.task.utils import list_files, load_targets, move_file
from tqdm import tqdm


class ImageDownloader(Node):
    """
    Node to download images from Bing for a set of target words.

    This node retrieves a specified number of images for each compound and its constituents,
    organizing them by compound in the output directory.

    Parameters:
        - output_dir: Directory where images are saved
        - targets: Dictionary (compound -> [constituents] or a YAML file path
        - num_images: Number of images to download per word
    """

    PARAMETERS = {"output_dir": str, "targets": dict | str, "num_images": int}

    def __init__(self, output_dir: str, targets: dict | str, num_images: int) -> None:
        self.output_dir = output_dir
        self.targets = targets if isinstance(targets, dict) else load_targets(targets)
        self.num_images = num_images

    def run(self) -> None:
        tmp_dir = join_paths(
            self.output_dir, "tmp"
        )  # Temporary directory for raw downloads

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
            compound_output_dir = join_paths(self.output_dir, compound)
            create_dir(compound_output_dir)

            # Move and rename each downloaded image into the compound's directory
            for word in words:
                word_dir = join_paths(tmp_dir, word)
                files = list_files(word_dir, True)

                for file in files:
                    file_number = file.split("_")[1].split(".")[0]
                    file_extension = file.split(".")[1]
                    file_input_path = join_paths(word_dir, file)
                    file_output_path = join_paths(
                        compound_output_dir, f"{word}_{file_number}.{file_extension}"
                    )
                    move_file(file_input_path, file_output_path)

                # Clean up temporary word directory
                remove_dir(word_dir)

        # Clean up the overall temp directory
        remove_dir(tmp_dir)
