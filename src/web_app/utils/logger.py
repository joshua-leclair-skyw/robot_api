import logging
import sys
from datetime import datetime as dt
from logging import DEBUG, INFO, ERROR, WARNING, StreamHandler


class Logger(object):
    def __init__(self, name, 
            format="%(asctime)s,%(msecs)d %(levelname)-9s"\
                   "[%(name)s] %(message)s",
            datefmt='%Y-%m-%d:%H:%M:%S',
            level=DEBUG):

        # TODO - add time rotating handler
        # TODO - print mode

        # Initial construct.
        self.format = format
        self.datefmt = datefmt
        self.name = name
        self.__level = level

        if(level == "Null"):
            self.level = DEBUG

        # Logger configuration.
        now = dt.now().strftime('%Y%m%d%H%M')
        self.file_formatter = logging.Formatter(self.format, self.datefmt)
        self.file_logger = logging.FileHandler(
            f"logs/{now}_robot_api.log", "a", "utf-8")
        self.file_logger.setFormatter(self.file_formatter)

        # Complete logging config.
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)
        self.logger.addHandler(self.file_logger)

    def debug(self, msg, extra=None):
        self.logger.debug(msg, extra=extra)
    
    def info(self, msg, extra=None):
        self.logger.info(msg, extra=extra)

    def warn(self, msg, extra=None):
        self.logger.warn(msg, extra=extra)
    
    def error(self, msg, extra=None):
        self.logger.error(msg, extra=extra)

    def critical(self, msg, extra=None):
        self.logger.critical(msg, extra=extra)

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, value):
        self.logger.setLevel(value)
        self.__level = value

    def print_logs(self):
        print_logger = logging.StreamHandler(sys.stdout)
        print_logger.setFormatter(self.file_formatter)
        self.logger.addHandler(print_logger)
