"""Application logging configuration."""

from __future__ import annotations

import logging
from pathlib import Path


LOG_FILE = Path("trading.log")


def setup_logging() -> None:
    """Configure file logging for the application.

    Calling this function multiple times is safe; logging.basicConfig only
    configures handlers once unless forced.
    """

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )

