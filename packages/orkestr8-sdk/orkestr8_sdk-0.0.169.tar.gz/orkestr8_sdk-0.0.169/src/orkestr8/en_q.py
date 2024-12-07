"""
Dynamic Queue to proivded 'data' visibility to the
running process. Could be described loosely as a
log aggregator
"""
import logging
import os
import queue
import re
import socket
import sys
import threading
import time
from multiprocessing import Process

from .utils import get_data_output_file, get_queue_pid_file

logger = logging.getLogger()


def file_worker(q: queue.Queue):
    last_epoch = None
    while True:
        with open(get_data_output_file()) as f:
            updated_epoch = None
            if lines := f.readlines():
                data = lines[-1]
                if re.search(r"\[data-row\]", data, flags=re.I):
                    updated_epoch = data
        if updated_epoch and last_epoch != updated_epoch:
            q.put(updated_epoch)
            last_epoch = updated_epoch

        time.sleep(1)


def start() -> None:
    """Kicks off process"""
    p = Process(target=_start)
    p.start()


def _start() -> None:
    """Worker code to invoke"""

    with open(get_queue_pid_file(), "w") as f:
        pid = os.getpid()
        f.write(f"PID: {pid}")

    q: queue.Queue[str] = queue.Queue()
    t = threading.Thread(target=file_worker, args=(q,))
    t.daemon = True
    t.start()

    sock = socket.socket()
    sock.settimeout(1)
    # TODO: MAKE DYNAMIC
    sock.bind(("localhost", 8000))
    sock.listen()

    try:
        while True:
            try:
                conn, _ = sock.accept()
            except socket.timeout:
                continue

            try:
                data: str = q.get_nowait()
            except queue.Empty:
                data = ""
            conn.sendall(data.encode())
    except KeyboardInterrupt:
        print("shutting down")
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        sys.exit()
