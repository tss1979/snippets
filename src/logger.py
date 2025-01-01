LOGGING_CONFIG = {
  "version": 1,
  "disable_existing_loggers": False,
  "filters": {...},
  "formatters": {
    "simple": {
      "format": "%(levelname)s: %(message)s",
      "datefmt": "%Y-%m-%dT%H:%M:%S%z"
    },
    "detailed": {
      "format": "[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
      "datefmt": "%Y-%m-%dT%H:%M:%S%z"
    }
  },
  "handlers": {
   "stderr": {
     "class": "logging.StreamHandler",
     "level": "WARNING",
     "formatter": "simple",
     "stream": "ext://sys.stderr"
   },
   "file": {
     "class": "logging.handlers.RotatingFileHandler",
     "level": "DEBUG",
     "formatter": "detailed",
     "filename": "../logs/my_app.log",
     "maxBytes": 10000,
     "backupCount": 3
   }
 },
  "loggers": {
    "root": {
      "level": "DEBUG",
      "handlers": [
        "stderr",
        "file",
      ],
    }
  }
}
