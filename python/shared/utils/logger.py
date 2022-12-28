import enum
import logging
import os
import os.path as path

from shared.consts import LOG_FOLDER

_LOG_PATH = path.join("", LOG_FOLDER)
_FORMAT_STRING = "%(asctime)s - [%(levelname)s] { logger: %(name)s; place: %(module)s.%(funcName)s:%(lineno)d } %(message)s"


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
        if not path.isdir(_LOG_PATH):
            os.mkdir(_LOG_PATH)

        self.logger = logging.getLogger(filename)
        self.logger.setLevel(level=level)
        self._handler = logging.FileHandler(
            f"{path.join(_LOG_PATH, filename)}.log", mode="w")
        self._formatter = logging.Formatter(_FORMAT_STRING)
        self._handler.setFormatter(self._formatter)
        self.logger.addHandler(self._handler)


Log = Logger(level="INFO", filename="main." +
             str(len(os.listdir(_LOG_PATH))))
