"""
utils/logger.py
───────────────
A shared logger used throughout the project.

WHY A CUSTOM LOGGER?
────────────────────
Python's logging module is powerful but verbose to configure.  This helper:
  • Adds colour output via `rich` so you can spot agent steps at a glance.
  • Provides a consistent format: [timestamp] LEVEL agent_name: message
  • Lets every module call get_logger(__name__) and get the same config.

USAGE
─────
    from utils.logger import get_logger
    log = get_logger(__name__)
    log.info("RAG retrieved 4 chunks")
    log.debug("Full state: %s", state)
"""

import logging
import sys
from rich.logging import RichHandler
from config import settings


def get_logger(name: str) -> logging.Logger:
    """Return a logger with the given name, configured with rich output."""
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if get_logger is called multiple times
    if logger.handlers:
        return logger

    level = logging.DEBUG if settings.debug_mode else logging.INFO
    logger.setLevel(level)

    handler = RichHandler(
        rich_tracebacks=True,
        show_path=False,        # hides the file:line in the output
        markup=True,            # allows [bold red]coloured[/] text in messages
    )
    handler.setLevel(level)

    formatter = logging.Formatter("%(message)s", datefmt="[%H:%M:%S]")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False    # don't double-print via root logger

    return logger
