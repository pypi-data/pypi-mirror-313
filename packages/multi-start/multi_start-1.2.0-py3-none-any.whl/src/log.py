import logging
import os

logging.basicConfig(level=logging.INFO, format="%(message)s")

logger = logging.getLogger("main")
logger.setLevel("DEBUG" if os.environ.get("DEBUG") else "INFO")
