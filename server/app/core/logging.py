import logging
import logging.config

from app.core.config import settings


def configure_logging() -> None:
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": (
                        "%(asctime)s | %(levelname)s | %(name)s | "
                        "%(message)s"
                    )
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": settings.LOG_FILE,
                    "maxBytes": 5_242_880,
                    "backupCount": 5,
                    "formatter": "default",
                    "encoding": "utf-8",
                },
            },
            "root": {
                "level": settings.LOG_LEVEL,
                "handlers": ["console", "file"],
            },
            "loggers": {
                "uvicorn.access": {
                    "level": settings.LOG_LEVEL,
                    "handlers": ["console", "file"],
                    "propagate": False,
                }
            },
        }
    )
