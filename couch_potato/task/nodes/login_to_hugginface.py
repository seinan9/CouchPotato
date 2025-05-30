import os

from couch_potato.core.node import Node
from huggingface_hub import login


class LoginToHuggingface(Node):
    """
    Node to authenticate with Hugging Face Hub.

    This node logs into the Hugging Face Hub using a provided token. The token can be
    passed explicitly via the `token` parameter or set as an environment variable `HF_TOKEN`.

    Parameters:
        - token (optional): Hugging Face access token
    """

    PARAMETERS = {"token": str}

    def __init__(self, token: str | None = None):
        # Use passed token or fall back to environment variable
        self.token = token or os.getenv("HF_TOKEN")
        if not self.token:
            raise RuntimeError(
                "You must set HF_TOKEN in your environment or pass it in the workflow."
            )

    def run(self):
        login(self.token)
