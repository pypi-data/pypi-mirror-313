from dataclasses import dataclass
from typing import Optional

from ..utils import get_pid_save_location
from .base import Command


@dataclass
class CheckArgs:
    file: Optional[str] = None


class CheckCommand(Command[CheckArgs]):
    @staticmethod
    def parse(args) -> CheckArgs:
        return CheckArgs(file=args.file)

    def run(self):
        file = self.args.file
        if file is None:
            file = get_pid_save_location()

        with open(file) as f:
            pid = f.read().split(":")[-1].strip()
        if pid:
            print("ACTIVE")
        else:
            print("INACTIVE")
