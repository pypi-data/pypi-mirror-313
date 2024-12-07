# Copyright (C) 2017 ETH Zurich
# Cosmology Research Group
# Author: Joerg Herbel, Silvan Fischbacher


import logging
import os
import sys

logging_levels = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
}


def get_logger(filepath, logging_level=None):
    """
    Get logger, if logging_level is unspecified, then try using the
    environment variable PYTHON_LOGGER_LEVEL.
    Defaults to info.
    :param filepath: name of the file that is calling the logger,
        used to give it a name.
    :return: logger object
    """

    if logging_level is None:
        if "PYTHON_LOGGER_LEVEL" in os.environ:
            logging_level = os.environ["PYTHON_LOGGER_LEVEL"]
        else:
            logging_level = "info"

    logger = logging.getLogger(os.path.basename(filepath)[:10])

    if len(logger.handlers) == 0:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(ColorFormatter())
        logger.addHandler(stream_handler)
        logger.propagate = False
        set_logger_level(logger, logging_level)

    logger.progressbar = Progressbar(logger)

    return logger


class ColorFormatter(logging.Formatter):
    RED = "\033[91m"
    VIOLET = "\033[95m"
    YELLOW = "\033[93m"
    ORANGE = "\033[33m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    reset = "\033[0m"
    format = "%(asctime)s %(name)10s %(levelname).3s   %(message)s "

    FORMATS = {
        logging.DEBUG: VIOLET + format + reset,
        logging.INFO: format,
        logging.WARNING: BOLD + ORANGE + format + reset,
        logging.ERROR: BOLD + RED + format + reset,
        logging.CRITICAL: BOLD + RED + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%y-%m-%d %H:%M:%S")
        return formatter.format(record)


class Progressbar:
    def __init__(self, logger=None):
        self.logger = logger

    def __call__(self, collection, at_level="info", **kw):
        kw.setdefault("bar_format", "{percentage:3.0f}%|{bar:28}|   {r_bar:<40} {desc}")
        kw.setdefault("disable", self.logger.level != logging_levels[at_level])
        kw.setdefault("colour", "blue")
        kw.setdefault("mininterval", 1)
        kw.setdefault("file", sys.stdout)
        from tqdm import tqdm

        return tqdm(collection, **kw)


def set_logger_level(logger, level):
    logger.setLevel(logging_levels[level])


def set_all_loggers_level(level):
    os.environ["PYTHON_LOGGER_LEVEL"] = level

    loggerDict = logging.root.manager.loggerDict
    for key in loggerDict:
        try:
            set_logger_level(logger=loggerDict[key], level=level)
        except Exception as err:
            LOGGER.debug(err)


LOGGER = get_logger(__file__)
