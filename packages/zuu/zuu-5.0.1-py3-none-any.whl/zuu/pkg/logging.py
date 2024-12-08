import logging
import sys


def basic_debug(level=10):
    """
    Sets up basic logging configuration with the specified logging level and stream.

    Args:
        level (int, optional): The logging level to set. Defaults to logging.DEBUG.
    """
    logging.basicConfig(level=level, stream=sys.stdout)
