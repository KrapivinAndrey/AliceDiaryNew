import logging
import os

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration


class LoggerFactory(object):
    _LOG = None

    @staticmethod
    def __create_logger(log_file, log_level):
        """
        A private method that interacts with the python
        logging module
        """
        # set the logging format
        log_format = "%(asctime)s:%(levelname)s:%(message)s"

        # Initialize the class variable with logger object
        LoggerFactory._LOG = logging.getLogger(log_file)
        logging.basicConfig(
            level=logging.INFO, format=log_format, datefmt="%Y-%m-%d %H:%M:%S"
        )

        # set the logging level based on the user selection
        if log_level == "INFO":
            LoggerFactory._LOG.setLevel(logging.INFO)
        elif log_level == "ERROR":
            LoggerFactory._LOG.setLevel(logging.ERROR)
        elif log_level == "DEBUG":
            LoggerFactory._LOG.setLevel(logging.DEBUG)

        if os.environ.get("SENTRY_DSN") is not None:
            sentry_logging = LoggingIntegration(
                level=logging.INFO, event_level=logging.WARN
            )
            sentry_sdk.init(
                dsn=os.environ.get("SENTRY_DSN"),
                integrations=[sentry_logging],
                environment=os.environ.get("ENVIRONMENT", "TEST"),
            )

        return LoggerFactory._LOG

    @staticmethod
    def get_logger(log_file):
        """
        A static method called by other modules to initialize logger in
        their own module
        """

        if os.environ.get("DEBUG") == "True":
            log_level = "DEBUG"
        else:
            log_level = "INFO"

        logger = LoggerFactory.__create_logger(log_file, log_level)

        # return the logger object
        return logger
