import logging

logger = logging.getLogger()


def setup_logger(level=logging.INFO):
    global logger
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)-5s] %(message)s"))
    logger.addHandler(handler)
