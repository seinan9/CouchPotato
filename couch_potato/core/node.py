from abc import ABC, abstractmethod


class Node(ABC):
    """
    Abstract base class for all nodes in the workflow.
    Each node must define required PARAMETERS, implement an initializer,
    and implement the run() method that executes the node's main logic.
    """

    # Dictionary specifying the parameters required by the node
    PARAMETERS = {}

    @abstractmethod
    def __init__(self) -> None:
        """
        Abstract constructor.
        Concrete node implementations should accept parameters
        defined in PARAMETERS and initialize their state accordingly.
        """

    @abstractmethod
    def run(self) -> None:
        """
        Abstract method to execute the node's task.
        Must be overridden by subclasses to provide node-specific behavior.
        """
