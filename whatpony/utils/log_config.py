from logging import Formatter

LOGGER_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": Formatter,
            "fmt": "%(name)s | %(asctime)s | %(levelname)s | %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default"
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": "logs/whatpony.log",
            "maxBytes": 1000000,
            "backupCount": 3,
            "encoding": "utf-8"
        }
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG"
    }
}