import importlib
import os
from dataclasses import dataclass
from multiprocessing import Process
from threading import Thread

from orkestr8.en_q import start as start_q
from orkestr8.utils import get_pid_save_location

from .base import Command


@dataclass
class TrainArgs:
    model_module: str


class TrainCommand(Command[TrainArgs]):
    @staticmethod
    def parse(args) -> TrainArgs:
        return TrainArgs(args.model_module)

    def _run(self):
        t = Thread(target=start_q)
        t.daemon = True
        t.start()

        m = importlib.import_module(self.args.model_module)
        child_id = os.getpid()
        with open(get_pid_save_location(), "w") as f:
            f.write(f"PID: {child_id}")
        m.train()

    def run(self):
        """Imports model training module and invokes 'train' function"""
        p = Process(target=self._run)
        p.start()
