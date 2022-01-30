from __future__ import unicode_literals
"""
Django settings for e-tender project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys
import urllib.parse

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DNS', ''),
    integrations=[DjangoIntegration()],
    send_default_pii=True,
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

DEBUG = False

ALLOWED_HOSTS = []

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'pipeline',
    'storages',
    'bootstrap4',
    'django_countries',
    'django_rq',
    'rest_framework',
    'assignment',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES_DIRS = (
    os.path.join(BASE_DIR, 'assignment', 'templates'),
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATES_DIRS,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DEFAULT_DATE_FORMAT = '%d/%m/%Y'
DATE_INPUT_FORMATS = (DEFAULT_DATE_FORMAT, )
REST_FRAMEWORK = {
    'DATE_INPUT_FORMATS': DATE_INPUT_FORMATS,
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

SITE_ID = 1
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # default
    'guardian.backends.ObjectPermissionBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, '.static')
STATIC_URL = os.environ.get('STATIC_URL', '/static/')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


PIPELINE = {
    'PIPELINE_ENABLED': True,
    'CSS_COMPRESSOR': None,
    'JS_COMPRESSOR': None,
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.CachedFileFinder',
    'pipeline.finders.PipelineFinder',
)

# Configuration for django-storages to use S3
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_S3_REGION_NAME = 'us-west-2'
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_CUSTOM_DOMAIN = urllib.parse.urlparse(STATIC_URL).netloc
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = 'public-read'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_REDIS_PREFIX = 'session:etender'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 days
SESSION_COOKIE_NAME = 'sessionid-etender'
SESSION_CACHE_ALIAS = 'session'

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
REDIS_EXPIRE_TIME = int(os.getenv('REDIS_EXPIRE_TIME', 60 * 30))
REDIS_DB = 0
REDIS = urllib.parse.urlparse(REDIS_URL)
EXCHANGE_RATE_API_CACHE_EXPIRY = 10 * 24 * 60 * 60# 10 days

OPEN_EXCHANGE_APP_ID = os.environ.get('OPEN_EXCHANGE_APP_ID')
# TODO : heroku throw error when database isn't 0 -- maybe since its free
RQ_REDIS_DB = 0
STATIC_FILES_REDIS_DB = 0
SESSION_REDIS_DB = 0

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # Redis url, ensure it has correct db number - Should be the form '<host>:<port>/<db>'
        'LOCATION': "{}/{}".format(REDIS_URL, REDIS_DB),
        'OPTIONS': {
            # "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            "CONNECTION_POOL_KWARGS": {
                "ssl_cert_reqs": None
            }
        },
        'KEY_PREFIX': 'etender',
        'TIMEOUT': 60 * 60 * 24,  # 1 day
    },
    'session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # Redis url, ensure it has correct db number - Should be the form '<host>:<port>/<db>'
        'LOCATION': "{}/{}".format(REDIS_URL, SESSION_REDIS_DB),
        'OPTIONS': {
            # "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            "CONNECTION_POOL_KWARGS": {
                "ssl_cert_reqs": None
            }
        },
        'KEY_PREFIX': SESSION_REDIS_PREFIX,
        'TIMEOUT': 60 * 60 * 24 * 30  # 30 days
    },
    'rq-cache': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # Redis url, ensure it has correct db number - Should be the form '<host>:<port>/<db>'
        'LOCATION': "{}/{}".format(REDIS_URL, 1),
        'OPTIONS': {
            # "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            "CONNECTION_POOL_KWARGS": {
                "ssl_cert_reqs": None
            }
        },
        'KEY_PREFIX': 'rq',
        'TIMEOUT': 60 * 20  # 20 min
    },
    'db-cache': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'db_cache_table',
        'TIMEOUT': 30 * 60,
    },
}

RQ_QUEUES = {
    'default': {
        'USE_REDIS_CACHE': 'rq-cache',
    },
}

RQ_SHOW_ADMIN_LINK = True
RQ_SCHEDULER_ENABLED = True

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


ENABLE_MAILING = os.environ.get('ENABLE_MAILING', 'True') == 'True'

EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'

HIVE_CONNECTION_STR = 'hive://localhost:10000/default'