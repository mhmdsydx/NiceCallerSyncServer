import logging
from config import LOG_FILE

logger = logging.getLogger("NiceCallerSync")

logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler = logging.FileHandler(LOG_FILE)

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def info(msg):
    logger.info(msg)


def error(msg):
    logger.error(msg)
