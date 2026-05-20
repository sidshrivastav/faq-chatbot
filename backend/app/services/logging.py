from __future__ import annotations

import logging
from typing import Any


def get_logger(name: str = "faq_assistant") -> logging.Logger:
    return logging.getLogger(name)


def log_event(logger: logging.Logger, event: str, **fields: Any) -> None:
    logger.info(event, extra={"event": event, **fields})
