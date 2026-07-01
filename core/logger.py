from __future__ import annotations

import logging
import os
import sys


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)

    if os.environ.get("JSON_LOG") or not sys.stderr.isatty():
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(
            logging.Formatter(
                '{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","msg":"%(message)s"}',
                datefmt="%Y-%m-%dT%H:%M:%S%z",
            )
        )
    else:
        from rich.console import Console
        from rich.logging import RichHandler

        console = Console(stderr=True)
        handler = RichHandler(
            console=console,
            show_time=True,
            show_path=False,
            rich_tracebacks=True,
        )
        handler.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(handler)
    return logger
