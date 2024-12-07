"""
Installs ML package on the machine by unzipping file and installing
"""
import logging
import subprocess
import sys

logger = logging.getLogger()


def install():
    with open("log.txt", "w") as f:
        logger.info("Installing foodenie_ml..")
        try:
            subprocess.run(["tar -xvzf foodenie_ml.tar.gz"], shell=True, stdout=f)
            subprocess.run(
                [
                    "cd foodenie_ml && python3 -m pip install -r requirements/prod.txt && rm ../foodenie_ml.tar.gz"
                ],
                shell=True,
                stdout=f,
            )
        except Exception as e:
            logger.error(
                f"Encountered installation error. {type(e).__name__:str(e)}.\nExiting..."
            )
            sys.exit(1)
    logger.info("Application install successfully. Existing installation script\n")
