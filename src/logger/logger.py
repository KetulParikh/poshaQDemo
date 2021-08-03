import logging
from logging.handlers import TimedRotatingFileHandler

def get_root_logger(logger_name, file_name=None):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] %(filename)s : %(lineno)d %(levelname)s - %(message)s','%B-%d %H:%M:%S')

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    if file_name:
        fh = TimedRotatingFileHandler(file_name, when="midnight", interval=1)
        fh.suffix = "%d_%B_%Y"
        fh_formatter = logging.Formatter('[%(asctime)s] %(filename)s : %(lineno)d %(levelname)s - %(message)s','%B-%d %H:%M:%S')
        fh.setFormatter(fh_formatter)
        fh.setLevel(logging.WARNING)
        logger.addHandler(fh)

    return logger
