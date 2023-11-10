import logging
import logging.handlers
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from api.config import CONSOLE_LOG_FORMAT, LOG_FORMAT, BASE_DIRECTORY


@dataclass
class LoggingSetup:
    name: str
    console_level: int = logging.ERROR
    file_level: int = logging.INFO
    console_format: str = CONSOLE_LOG_FORMAT
    file_format: str = LOG_FORMAT
    file_name: Optional[str] = None
    max_file_size_in_bytes: int = 1024 * 1024
    file_backup_count: int = 16
    log_directory: Path = BASE_DIRECTORY.joinpath("logs").absolute()
    os.makedirs(log_directory, exist_ok=True)

    def get_effective_log_level(self):
        return min(self.console_level, self.file_level)


def get_logger(log_config: LoggingSetup) -> logging.Logger:
    """
    Create a logger and return.
    Arguments:
        log_config: configuration object of a logger
    Return:
        logger: the created logger
    """
    new_logger = logging.getLogger(
        name=log_config.name
    )
    if new_logger.handlers:
        new_logger.warning("This logger is already set up")
        return new_logger

    new_logger.setLevel(log_config.get_effective_log_level())
    new_logger.propagate = False
    stream_formatter = logging.Formatter(log_config.console_format)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(stream_formatter)
    stream_handler.setLevel(log_config.console_level)

    new_logger.addHandler(stream_handler)
    if log_config.file_name is None:
        log_config.file_name = log_config.name.lower() + ".log"
        logging.warning(
            "No file specified, defaulting to '%s'", log_config.file_name
        )

    file_name = log_config.log_directory.joinpath(log_config.file_name)
    file_formatter = logging.Formatter(log_config.file_format)

    file_handler = logging.handlers.RotatingFileHandler(
        file_name, maxBytes=log_config.max_file_size_in_bytes,
        backupCount=log_config.file_backup_count
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(log_config.file_level)

    new_logger.addHandler(file_handler)
    new_logger.debug("Logger %s has been created", new_logger.name)
    return new_logger


def get_logger_by_name(name: str):
    log_config = LoggingSetup(name=name)
    return get_logger(log_config)


logger = get_logger_by_name("calorie-compass")
