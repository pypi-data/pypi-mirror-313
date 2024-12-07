from logging import ERROR, getLogger
from logging.config import dictConfig

from trainerbase.config import CONFIG_FILE, config_warnings, logging_config


if logging_config is None:
    logging_config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] <%(levelname)s> %(funcName)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "console": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"],
        },
    }
    using_default_config = True
else:
    using_default_config = False


dictConfig(logging_config)
getLogger("comtypes").setLevel(ERROR)

logger = getLogger("TrainerBase")

if using_default_config:
    logger.debug(f"No logging config in {CONFIG_FILE}! Using default one.")

for warning_message in config_warnings:
    logger.warning(warning_message)
