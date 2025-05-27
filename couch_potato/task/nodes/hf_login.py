import os

from couch_potato.core.node import Node
from huggingface_hub import login


class HfLogin(Node):
    PARAMETERS = {"token": str}  # optional override

    def __init__(self, token: str | None = None):
        self.token = token or os.getenv("HF_TOKEN")
        if not self.token:
            raise RuntimeError(
                "You must set HF_TOKEN in your environment or pass it in the workflow."
            )

    def run(self):
        login(self.token)
