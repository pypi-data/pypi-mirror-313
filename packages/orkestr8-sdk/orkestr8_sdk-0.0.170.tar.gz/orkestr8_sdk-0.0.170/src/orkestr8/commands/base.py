from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Command(Generic[T], ABC):
    def __init__(self, args) -> None:
        self.args: T = self.parse(args)

    @staticmethod
    @abstractmethod
    def parse(args) -> T:
        """Parse args from cli to command type"""

    @abstractmethod
    def run(self):
        """The 'dispatch' command to be invoked"""
