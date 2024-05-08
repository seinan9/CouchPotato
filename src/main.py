import argparse
import logging

from core.engine import Engine
from core.utils import load_config


if __name__ == "__main__":

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO)

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-f',
        '--file',
        help='A yaml file containing the workflows.',
        default='ImageCompositionality/default.yaml')
    args = argparser.parse_args()

    config = load_config(args.file)
    engine = Engine(config)
    engine.start()
