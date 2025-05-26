from couch_potato.core.node import Node


class ExampleNode(Node):

    PARAMETERS = {"message": str}

    def __init__(self, message: str) -> None:
        self.message = message

    def run(self):
        print(self.message)
