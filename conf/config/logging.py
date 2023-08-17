import os
DEBUG = os.getenv("DEBUG", True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "\033[1;32m{levelname:5s}\033[0m  \033[0;32m{asctime}\033[0m {name} {pathname}:{lineno} \n\033[0;32m{message}\033[0m",
            "style": "{",
        },
        "simple": {
            "format": "{levelname:5s} {asctime} -> {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose" if DEBUG else "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "asyncio": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
        },
        "daphne": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
        },
        "urllib3": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
        },
        "docker": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
        },
        "root": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "INFO",
        },
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
