import logging
import os
import time
from dataclasses import dataclass
from typing import Callable, Dict, Union

from orkestr8.utils import get_pid_save_location, get_queue_pid_file

from .base import Command

PROCESSES: Dict[str, Callable] = {
    "TRAINING_PROCESS": get_pid_save_location,
    "QUEUE_PROCESS": get_queue_pid_file,
}

LOGGER = logging.getLogger()


def _shut_down_processes() -> None:
    """Fetches PIDs from their saved file
    location and kills processes"""
    for process_name, file_fn in PROCESSES.items():
        with open(file_fn()) as f:
            pid = f.read().split(":")[-1].strip()
        if pid:
            os.remove(file_fn())
            for _ in range(10):
                if not os.path.exists(f"/proc/{pid}"):
                    LOGGER.info(
                        f"Process {pid} has terminated. '{process_name}' has stopped"
                    )
                    break
                time.sleep(1)


@dataclass
class StopArgs:
    pid: Union[str, None]


class StopCommand(Command[StopArgs]):
    @staticmethod
    def parse(args) -> StopArgs:
        return StopArgs(args.pid)

    def run(self):
        LOGGER.info("Shutdown command invoked")
        _shut_down_processes()
        LOGGER.info("Process shutdown complete")
