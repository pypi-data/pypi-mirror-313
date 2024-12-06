import logging

import colorlog

LOG_NAME = "TTXT_V2"


class Initializer:
    @staticmethod
    def init_logger() -> logging.Logger:
        """
        Initializes and configures a logger with a colored console output.

        Returns:
            logging.Logger: Configured logger instance with the name 'TTXT_V2'.
        """
        log = logging.getLogger(LOG_NAME)
        log.setLevel(logging.DEBUG)
        cout_handler = logging.StreamHandler()
        cout_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                "DEBUG": "bold_white",
                "INFO": "bold_green",
                "WARNING": "bold_yellow",
                "ERROR": "bold_red",
                "CRITICAL": "bold_purple",
            },
        )
        cout_handler.setFormatter(cout_formatter)
        log.addHandler(cout_handler)
        return log


logger = Initializer.init_logger()
