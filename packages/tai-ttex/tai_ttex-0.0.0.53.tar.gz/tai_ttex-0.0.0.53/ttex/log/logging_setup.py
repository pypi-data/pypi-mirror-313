"""Convenient setup for python logging module"""
import logging
import logging.config
import copy
from typing import cast

logging_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(filename)s"
            + " - %(funcName)s - %(threadName)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "root_console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "DefaultLogger": {
            "level": "WARNING",
            "handlers": ["console"],
        },
    },
    "root": {
        "level": "WARNING",
        "handlers": ["root_console"],
    },
}


def initiate_logger(log_level: int):
    """
    Convenience function to set the logging level of a given logger

    Parameters:
      * logger: logging.Logger
      * log_level: The log level to set to in [0,10, 20, 30, 40, 50]

    For more information on log levels see
    https://docs.python.org/3/library/logging.html#logging-levels
    If given log level is not recognised, set to default
    """

    config = cast(dict, copy.deepcopy(logging_config))

    chosen_level = logging.getLevelName(log_level)
    chosen_level_exists = chosen_level != f"Level {log_level}"
    if chosen_level_exists:  # Level exists - so change accordingly
        config["loggers"]["DefaultLogger"]["level"] = chosen_level
        config["handlers"]["console"]["level"] = chosen_level

    logging.config.dictConfig(config)

    logger = logging.getLogger("DefaultLogger")
    if chosen_level_exists:
        logger.debug(f"Set up log level for {log_level}")
    else:
        logger.error(
            f"Chosen log level {log_level} does not exist. "
            + "Logger level remains at "
            + f"{logger.getEffectiveLevel()}. Options are listed "
            + "here https://docs.python.org/3/library/logging.html#logging-levels"
        )
