import logging
from yfa.config import config


def configure_logging():
    if config.LOG_LEVEL == "DEBUG":
        # log level:logged message:full module path:function invoked:line number of logging call
        LOGFORMAT = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"
        logging.basicConfig(level=config.LOG_LEVEL, format=LOGFORMAT)
    else:
        logging.basicConfig(level=config.LOG_LEVEL)
