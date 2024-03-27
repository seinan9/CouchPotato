import argparse
import logging


class ArgParser:

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

        self.argparser = argparse.ArgumentParser()
        self.argparser.add_argument(
            '-f',
            '--file',
            help='A yaml file containing the workflows.',
            default='./workflow_config.yaml'
        )

    def parse_args(self):
        self.logger.info('Parsing arguments')
        return self.argparser.parse_args()
