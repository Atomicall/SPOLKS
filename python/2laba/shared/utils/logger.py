import enum
import logging
import os
from os import path

from shared.consts import LOG_FOLDER

_LOG_PATH = path.join("", LOG_FOLDER)
_FORMAT_STRING = "%(name)s %(asctime)s %(levelname)s %(message)s"


class LOG_LEVELS(enum.Enum):
    NONSET = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


class Logger():
    logger: logging.Logger
    _handler: logging.FileHandler
    _formatter: logging.Formatter

    def __init__(self, filename: str, level: str):
        if not path.isdir(LOG_FOLDER):
            os.mkdir(LOG_FOLDER)
        self.logger = logging.getLogger(filename)
        self.logger.setLevel(level=level)
        self._handler = logging.FileHandler(
            f"{filename}.log", mode="w")
        self._formatter = logging.Formatter(_FORMAT_STRING)
        self._handler.setFormatter(self._formatter)
        self.logger.addHandler(self._handler)
