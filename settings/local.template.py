from __future__ import unicode_literals
from .base import *

WSGI_APPLICATION = u'wsgi.local.application'

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h!vt!tpdr_5%&fxq5e#5x&%53#l_(&=5-ja)-a3m_b_ync+0v-'

DEFAULT_FILE_STORAGE = u'django.core.files.storage.FileSystemStorage'

DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'NAME': 'football_assignment',
            'ENFORCE_SCHEMA': True,
            'CLIENT': {
                'host': 'mongodb+srv://USERNAME:PASSWORD@aui-de-assignments.cohiy.mongodb.net/admin'
            }
        }
}


LOGGING = {
    'version': 1,
    "disable_existing_loggers": True,
    'root': {
        'level': 'INFO',
        'handlers': ['console', ],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(name)s %(processName)s %(message)s',
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout,
        },
        'rq_console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null', ],
            'propagate': False,
            'level': 'INFO',
        },
        'django.db.backends': {
            'handlers': ['console', ],
            'level': 'INFO',
            'propagate': False,
        },
        'boto': {
            'handlers': ['console', ],
            'level': 'INFO',
            'propagate': False,
        },
        'rq.worker': {
            'handlers': ['rq_console', ],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

ANYMAIL = {
    'MAILGUN_API_KEY': '',
    'MAILGUN_API_URL': 'https://api.mailgun.net/v3/',
    'MAILGUN_SENDER_DOMAIN': "shippion.com",
}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
DEFAULT_FROM_EMAIL = 'e-tender@shippion.com'
