import datetime
import logging
from pathlib import Path
import sys
from typing import Any, MutableMapping, Optional


try:
    sys.stdout.reconfigure(line_buffering=False)  # type: ignore
except Exception:
    pass


Logger = logging.Logger | logging.LoggerAdapter


# Simple adapter that supports adding a single string-formattable object as context
class LogContextAdapter(logging.LoggerAdapter):
    def __init__(self, logger: Logger, context: Any):
        super().__init__(logger)
        self.context = context

    def process(self, msg, kwargs) -> tuple[Any, MutableMapping[str, Any]]:
        return (f"[{self.context}] {msg}", kwargs)


def make_logger(
    name: str,
    stdout: Optional[int],
    file: Optional[Path] = None,
    format: str = "%(message)s",
) -> logging.Logger:
    logger = logging.getLogger(name)

    # Prevent duplicate initializations
    if logger.hasHandlers() and logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(format)

    if stdout:
        handler: logging.Handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if file:
        handler = logging.FileHandler(file)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    # Prevents logging from propagating to the root logger, which would cause logs to appear in stdout if basicConfig is called, even though we're not adding stdout handler
    logger.propagate = False

    logger.debug(f"START {name} {datetime.datetime.today()}")

    return logger
