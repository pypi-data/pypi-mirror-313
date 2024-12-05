"""Logger."""
import logging
import os

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logger = logging.getLogger("ithaca_sdk")
logger.setLevel(getattr(logging, log_level, logging.INFO))

ch = logging.StreamHandler()
ch.setLevel(getattr(logging, log_level, logging.INFO))

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch.setFormatter(formatter)

logger.addHandler(ch)
logger.propagate = False
