import sys
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from loguru import Logger
else:
    Logger = None


def logger_factory() -> Logger:
    logger.remove()
    logger.add(
        sys.stdout,
        level="DEBUG",
    )

    return logger
