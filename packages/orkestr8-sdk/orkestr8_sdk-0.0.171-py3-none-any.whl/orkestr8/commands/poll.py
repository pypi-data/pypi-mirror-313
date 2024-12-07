from ..en_q_client import poll
from .base import Command


class PollArgs:
    pass


class PollCommand(Command[PollArgs]):
    """Command used to retrive training data in
    SDK queue on server"""

    @staticmethod
    def parse(args):
        pass

    def run(self):
        data = poll()
        # send to output stream
        print(data)
