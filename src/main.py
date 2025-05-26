import argparse
import logging

from ImageCompositionality.src.core.engine import Engine
from ImageCompositionality.src.core.utils import load_config

PROGRESS = 25
logging.addLevelName(PROGRESS, "PROGRESS")


def progress(self, message, *args, **kwargs):
    if self.isEnabledFor(PROGRESS):
        formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")
        print(
            formatter.format(
                logging.LogRecord(
                    self.name, PROGRESS, "", 0, message + "\r", args, None
                )
            ),
            end="",
            flush=True,
        )


if __name__ == "__main__":

    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    logging.Logger.progress = progress

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-f",
        "--file",
        help="A yaml file containing the workflows.",
        default="ImageCompositionality/default.yaml",
    )
    args = argparser.parse_args()

    config = load_config(args.file)
    engine = Engine(config)
    engine.start()
