from couch_potato.core.node import Node


class Print(Node):
    """
    Node that prints a given message to the console.
    """

    PARAMETERS = {"message": str}

    def __init__(self, message: str) -> None:
        self.message = message

    def run(self):
        print(self.message)
