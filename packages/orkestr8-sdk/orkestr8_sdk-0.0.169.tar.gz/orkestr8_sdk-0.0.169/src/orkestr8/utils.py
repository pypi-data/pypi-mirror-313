import os
from pathlib import Path

from .settings import (
    DATA_OUTPUT_FILE_LOCATION,
    PID_FILE_LOCATION,
    QUEUE_PID_FILE_LOCATION,
)


def __create_file_if_not_exists(file_path: Path) -> None:
    """Wrapper to ensure `file_path` exists, even if empty"""
    if Path(file_path).exists():
        return
    os.makedirs(str(file_path.parent), exist_ok=True)
    with open(str(file_path), "w"):
        pass


def get_pid_save_location() -> Path:
    __create_file_if_not_exists(PID_FILE_LOCATION)
    return PID_FILE_LOCATION


def get_data_output_file() -> Path:
    __create_file_if_not_exists(DATA_OUTPUT_FILE_LOCATION)
    return DATA_OUTPUT_FILE_LOCATION


def get_queue_pid_file() -> Path:
    __create_file_if_not_exists(QUEUE_PID_FILE_LOCATION)
    return QUEUE_PID_FILE_LOCATION
