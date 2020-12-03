import configparser
import logging

DEFAULT_LOGGER_NAME = 'ImageProcessor'
LOG_FILE_NAME = 'ImageProcessor.log'
DEFAULT_LOG_FORMATTER = '%(asctime)s - %(relativeCreated)6d - %(threadName)s - %(levelname)s - %(message)s'
__is_configured = False


def initialize(config: configparser.ConfigParser) -> None:
    global __is_configured
    if __is_configured:
        return

    logging_level = config['logging']['level']
    logger = logging.getLogger(DEFAULT_LOGGER_NAME)
    logger.setLevel(logging_level)

    formatter = logging.Formatter(DEFAULT_LOG_FORMATTER)

    __add_file_handler(formatter, logger, logging_level)

    if config.getboolean('logging', 'log_to_console'):
        __add_console_handler(formatter, logger, logging_level)

    __is_configured = True


def __add_console_handler(formatter: logging.Formatter, logger: logging.Logger, logging_level: str) -> None:
    ch = logging.StreamHandler()
    ch.setLevel(logging_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def __add_file_handler(formatter: logging.Formatter, logger: logging.Logger, logging_level: str) -> None:
    fh = logging.FileHandler(LOG_FILE_NAME)
    fh.setLevel(logging_level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def get_logger() -> logging.Logger:
    if not __is_configured:
        raise RuntimeError('Logger must be initialized first!')

    return logging.getLogger(DEFAULT_LOGGER_NAME)
