"""Loggers configuration"""
import logging
from logging.handlers import TimedRotatingFileHandler
import sys


def init_logger(
        file_path: str,
        name: str = "app",
        stream_level: int = logging.DEBUG,
        file_level: int = logging.WARNING
):
    """Initialize the logger"""
    logging.getLogger(name).setLevel(min(stream_level, file_level))
    formatter = logging.Formatter(
        "[%(filename)s:%(lineno)d (%(funcName)s)] %(asctime)s %(levelname)s \t %(message)s"
    )
    file_handler = TimedRotatingFileHandler(filename=file_path, when="D", interval=3, backupCount=0)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(file_level)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(stream_level)
    logging.getLogger(name).addHandler(file_handler)
    logging.getLogger(name).addHandler(stream_handler)
