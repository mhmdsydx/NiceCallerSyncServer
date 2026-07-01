import logging

from config import LOG_FILE

logger = logging.getLogger("NiceCallerSync")

logger.setLevel(logging.INFO)

formatter = logging.Formatter(

    "%(asctime)s | %(levelname)s | %(message)s"

)

handler = logging.FileHandler(LOG_FILE)

handler.setFormatter(formatter)

logger.addHandler(handler)


def info(msg):

    logger.info(msg)

    print(msg)


def error(msg):

    logger.error(msg)

    print(msg)
