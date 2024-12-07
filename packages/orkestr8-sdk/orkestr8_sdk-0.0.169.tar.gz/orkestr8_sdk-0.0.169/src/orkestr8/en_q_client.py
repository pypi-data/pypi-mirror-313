"""
Client to communicate with SDK created Python Queue.

RUN STATES:
- GET: retreives data
- STOP: Sends message to shutdown
"""
import socket
import time


def poll():
    sock = socket.socket()
    sock.connect(("localhost", 8000))
    sock.setblocking(False)
    data = ""
    x = 1
    while x < 5:
        x += 1
        try:
            data = sock.recv(1024)
        except BlockingIOError:
            pass
        else:
            if data:
                sock.close()
                break
        time.sleep(0.5)
    return data
