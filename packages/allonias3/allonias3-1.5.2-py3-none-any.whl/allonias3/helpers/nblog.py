import logging
from typing import Literal


def nb_log(
    level: Literal[
        "CRITICAL",
        "FATAL",
        "ERROR",
        "WARN",
        "WARNING",
        "INFO",
        "DEBUG",
        "NOTSET",
    ] = "INFO",
):
    """Enables logging inside the notebook.

    Without it, allonias3 messages will not be printed.

    Args:
        level (str): A valid logger level, defaults to "INFO".

    Returns:
        :
            The logger object
    """
    logger = logging.getLogger()
    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
