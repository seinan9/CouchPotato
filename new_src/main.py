import logging

from engine import Engine
from argparser import ArgParser
from utils import Utils

if __name__ == "__main__":

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO)

    argparser = ArgParser()
    args = argparser.parse_args()
    workflow_config = Utils.load_config(args.file)
    engine = Engine(workflow_config)
    engine.start()
