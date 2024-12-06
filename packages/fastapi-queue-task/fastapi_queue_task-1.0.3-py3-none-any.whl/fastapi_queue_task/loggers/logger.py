import logging

from ..loggers.format import LoggerFormatter

logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(LoggerFormatter())
logger.addHandler(stream_handler)
