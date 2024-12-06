"""Top-level package for T - Page Object."""
import logging
import sys

log_format = logging.Formatter("[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s")
log_level = logging.DEBUG

logger = logging.getLogger("t_page_object")
if logger.hasHandlers():
    logger.handlers = []
logger.setLevel(log_level)
logger.propagate = False

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(log_level)
handler.setFormatter(log_format)
logger.addHandler(handler)

__author__ = """Thoughtful"""
__email__ = "support@thoughtful.ai"
__version__ = "__version__ = '0.2.0'"
