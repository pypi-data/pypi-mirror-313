import os
import logging
from typing import Tuple
from logging import StreamHandler, Formatter
from logging.handlers import WatchedFileHandler

from phound.config import settings

_PHOUND_LOGGER_NAME = "phound"

logger: logging.Logger = logging.getLogger(_PHOUND_LOGGER_NAME)


def setup_logging() -> None:
    handler = StreamHandler()
    handler.setFormatter(_get_formatter())
    logger.addHandler(handler)
    logger.setLevel(logging.ERROR)

    is_logging_enabled, log_file_dir = get_logging_parameters()
    if not is_logging_enabled:
        return

    logger.setLevel(logging.DEBUG)
    logger.info(f"Set {logging.DEBUG} level to logger: {_PHOUND_LOGGER_NAME}")

    # WatchedFileHandler is only intended for use under Unix/Linux
    if log_file_dir and os.name == 'posix':
        _setup_file_handler(f"{log_file_dir}/phound-all.log", logging.DEBUG)
        _setup_file_handler(f"{log_file_dir}/phound-error.log", logging.ERROR)
        logger.info(f"Added a file logging handlers to logger: {_PHOUND_LOGGER_NAME}")


def get_logging_parameters() -> Tuple[bool, str]:
    return (settings.phound_log,
            _to_absolute_path(settings.phound_log_dir))


def _setup_file_handler(path: str, level: int) -> None:
    handler = WatchedFileHandler(path)
    handler.setFormatter(_get_formatter())
    handler.setLevel(level)
    logger.addHandler(handler)


def _get_formatter() -> Formatter:
    return Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] "
                     "[thread:%(threadName)s] [%(filename)s:%(lineno)d] %(message)s")


def _to_absolute_path(log_file_dir: str) -> str:
    return os.path.abspath(log_file_dir) if log_file_dir else ""
