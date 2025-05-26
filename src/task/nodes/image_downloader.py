import logging

from bing_image_downloader import downloader

from ImageCompositionality.src.core.node import Node
from ImageCompositionality.src.core.utils import create_dir, join_paths, remove_dir
from ImageCompositionality.src.task.utils import list_files, load_targets, move_file


class ImageDownloader(Node):

    PARAMETERS = {"output_dir": str, "targets": dict | str, "num_images": int}

    def __init__(self, output_dir: str, targets: dict | str, num_images: int) -> None:
        self.logger = logging.getLogger(__name__)
        self.output_dir = output_dir
        self.targets = targets if isinstance(targets, dict) else load_targets(targets)
        self.num_images = num_images

    def run(self) -> None:
        progress = 0
        num_targets = len(self.targets)
        tmp_dir = join_paths(self.output_dir, "tmp")
        for compound, constituents in self.targets.items():
            progress += 1
            self.logger.progress(f"Processing target {progress} out of {num_targets}")

            for word in [compound] + constituents:
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

            compound_output_dir = join_paths(self.output_dir, compound)
            create_dir(compound_output_dir)

            for word in [compound] + constituents:
                word_dir = join_paths(self.output_dir, "tmp", word)
                files = list_files(word_dir, True)
                for file in files:
                    file_number = file.split("_")[1].split(".")[0]
                    file_extension = file.split(".")[1]
                    file_input_path = join_paths(word_dir, file)
                    file_output_path = join_paths(
                        compound_output_dir, f"{word}_{file_number}.{file_extension}"
                    )
                    move_file(file_input_path, file_output_path)
                remove_dir(word_dir)
        remove_dir(tmp_dir)
        remove_dir(tmp_dir)
