# Copyright ZettaBlock Labs 2022
import logging


def configure_logger(logger: logging.Logger, log_level: str):
    ch = logging.StreamHandler()
    log_level_numeric = logging.getLevelName(log_level.upper())
    logger.setLevel(log_level_numeric)
    ch.setLevel(log_level_numeric)
    ch.setFormatter(
        logging.Formatter(
            "[%(threadName)s] %(asctime)s %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z"
        )
    )
    logger.addHandler(ch)


logger = logging.getLogger("zetta-utils")
configure_logger(logger, "[INFO]")
