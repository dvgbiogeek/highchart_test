from .base import *

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s: %(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file1': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
            'formatter': 'verbose'
        },
        'file2': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'protein.log',
            'formatter': 'verbose'
        },
        'syslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'verbose',
            'address': ('frozen-stream-5430.papertrailapp.com', 11111)
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file1'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'composition': {
            'handlers': ['file2'],
            'level': 'DEBUG',
        },
        'glossary': {
            'handlers': ['file2'],
            'level': 'DEBUG',
        },
        'account': {
            'handlers': ['file2'],
            'level': 'DEBUG',
        }
    }
}
