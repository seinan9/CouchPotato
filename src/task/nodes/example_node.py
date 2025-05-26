from ImageCompositionality.src.core.node import Node


class ExampleNode(Node):

    PARAMETERS = {"name": str, "age": int}

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def run(self):
        print(self.name, self.age)
