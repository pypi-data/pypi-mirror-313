import sys

from loguru import logger


def set_logging_level(level, to_file=False):
    logger.remove()  # Remove current logger
    logger.add(sys.stderr, level=level)  # Reconfigure with the new level

    if to_file:
        logger.add(
            "bic.log",
            mode="w",
            # compression="zip",
            level=level,
        )


def get_level_names():
    return ["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]
