LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DEFAULT_HANDLERS = ['console', ]

# В логгере настраивается логгирование pywsgi-сервера.
# Про логирование в Python можно прочитать в документации
# https://docs.python.org/3/howto/logging.html
# https://docs.python.org/3/howto/logging-cookbook.html

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': LOG_FORMAT
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'level': 'INFO',
        'formatter': 'verbose',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}
