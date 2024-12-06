import logging

from mach_client.log import (
    LogContextAdapter,
    Logger,
    make_logger
)

from . import config


# Default logger for this project
logger: Logger = make_logger("cctt", logging.INFO, config.log_file)
