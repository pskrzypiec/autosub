"""as_logging.py - logging for Autosub module"""
import os
import logging
from time import strftime

TRACES_FILENAME = \
    os.path.dirname(os.path.dirname(__file__)) + \
    r'/logs/autosub_' + strftime("%Y%m%d_%H%M%S") + r'.log'


class MyLogger:
    """MyLogger class"""

    logger = logging.getLogger('subget')
    file_handler = logging.FileHandler('/var/tmp/subget.log')
    file_handler_app = \
        logging.FileHandler(TRACES_FILENAME, mode='a', encoding='utf-8', delay=False)
    console_handler = logging.StreamHandler()

    def __init__(self, handlers=None):

        if handlers is None:
            self.logger.setLevel(logging.DEBUG)  # (! needed for differentiate level later)

            self.file_handler.setLevel(logging.DEBUG)
            self.file_handler_app.setLevel(logging.DEBUG)
            self.console_handler.setLevel(logging.INFO)  # differentiate handler logging level

            # create formatter and add them to the handlers
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            self.file_handler.setFormatter(formatter)
            self.file_handler_app.setFormatter(formatter)
            self.console_handler.setFormatter(formatter)

            # add the handlers to the logger
            self.logger.addHandler(self.file_handler)
            self.logger.addHandler(self.file_handler_app)
            self.logger.addHandler(self.console_handler)
        else:
            print(handlers)

    def console_output_enabled(self, enabled=True):
        """Toggle console output"""

        if enabled:
            self.logger.addHandler(self.console_handler)
        else:
            self.logger.removeHandler(self.console_handler)

    def console_output_level(self, level=logging.INFO):
        """Set console output logging level"""

        self.console_handler.setLevel(level)
