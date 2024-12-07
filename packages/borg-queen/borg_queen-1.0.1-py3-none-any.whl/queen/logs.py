import logging
import os.path
import sys
from logging.config import dictConfig

logger = logging.getLogger("queen")


def config(log_directory, log_stdout):
    handlers = []
    if log_stdout:
        handlers += ["stdout"]
    if log_directory:
        handlers += ["file", "file_verbose"]
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "verbose": {"format": "%(levelname)s %(asctime)s %(message)s"},
            },
            "handlers": {
                "file": {
                    "class": "logging.FileHandler",
                    "formatter": "verbose",
                    "filename": os.path.join(log_directory, "queen.log"),
                    "level": "INFO",
                },
                "file_verbose": {
                    "class": "logging.FileHandler",
                    "formatter": "verbose",
                    "filename": os.path.join(log_directory, "queen_verbose.log"),
                    "level": "DEBUG",
                },
                "stdout": {
                    "class": "logging.StreamHandler",
                    "formatter": "verbose",
                    "stream": sys.stdout,
                    "level": "DEBUG",
                },
            },
            "loggers": {
                "queen": {
                    "handlers": handlers,
                    "level": "DEBUG",
                },
            },
        }
    )
