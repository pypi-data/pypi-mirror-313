import logging
import os
import sys
from enum import Enum
from typing import Dict, List, Type

import dotenv

from orkestr8.cli import parse_args
from orkestr8.commands.base import Command
from orkestr8.commands.check import CheckCommand
from orkestr8.commands.download_model import DownloadModelCommand
from orkestr8.commands.poll import PollCommand
from orkestr8.commands.stop import StopCommand
from orkestr8.commands.test import TestCommand
from orkestr8.commands.train import TrainCommand
from orkestr8.commands.update import UpdateCommand

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format="[%(asctime)s]:%(message)s")


class Dispatch(Enum):
    TRAIN = "train"
    RUN = "run"
    UPDATE = "update"
    STOP = "stop"
    DOWNLOAD_MODEL = "download_model"
    CHECK = "check"
    POLL = "poll"
    MOCK_RUN = "mock_run"


# Order of commands only matters in list, if multiple are provided
DISPATCH_MAP: Dict[Dispatch, List[Type[Command]]] = {
    Dispatch.TRAIN: [TrainCommand],
    Dispatch.RUN: [UpdateCommand, TrainCommand],
    Dispatch.UPDATE: [UpdateCommand],
    Dispatch.STOP: [StopCommand],
    Dispatch.DOWNLOAD_MODEL: [DownloadModelCommand],
    Dispatch.CHECK: [CheckCommand],
    Dispatch.POLL: [PollCommand],
    Dispatch.MOCK_RUN: [TestCommand],
}

dotenv.load_dotenv()


def handle_env_vars(args):
    check_env_variables(args)


# TODO: ELminate this method
# some commands dont require this
def check_env_variables(args):
    required_variables = ["AWS_ACCESS_KEY", "AWS_SECRET_KEY", "AWS_BUCKET_NAME"]

    for v in required_variables:
        if not os.environ.get(v):
            attr = getattr(args, v.lower(), None)
            if attr:
                os.environ[v] = attr


def run(args) -> None:
    # TODO: This could be dynamic. Ensure
    # Underlying package is in system path
    sys.path.append(os.getcwd() + "/foodenie_ml")

    commands_to_run: List[Type[Command]] = []
    command = Dispatch(args.command)
    commands_to_run = DISPATCH_MAP[command]

    for command_cls in commands_to_run:
        c = command_cls(args)
        c.run()


def main():
    args = parse_args()
    logger.debug(args)
    handle_env_vars(args)
    run(args)


if __name__ == "__main__":
    main()
