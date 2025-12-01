import logging
import sys

def setup_logging():
    logger = logging.getLogger("ayushman_rag")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '{"level":"%(levelname)s","time":"%(asctime)s","message":"%(message)s"}'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

logger = setup_logging()
