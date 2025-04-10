from logging.config import dictConfig

LOGGING_CONFIG = {
    # configurações de log
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "%(levelname)s - %(asctime)s - %(name)s - %(message)s"},
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(message)s"},
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}


def setup_logging():
    """Configura o logging"""
    dictConfig(LOGGING_CONFIG)
