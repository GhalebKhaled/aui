from __future__ import unicode_literals
from .base import *

import dj_database_url


WSGI_APPLICATION = u'wsgi.local.application'

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h!vt!tpdr_5%&fxq5e#5x&%53#l_(&=5-ja)-a3m_b_ync+0v-'

# TODO this should be seperate database
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres://ubuntu@localhost:5432/circle_test')
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL),
}

DATABASES['default']['CONN_MAX_AGE'] = None

MEDIA_ROOT = os.path.join(BASE_DIR, 'tenders/tests/resources')

# circleci fails at 'ssl_cert_reqs' -- I think we need to enable TLS connection on circleci redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # Redis url, ensure it has correct db number - Should be the form '<host>:<port>/<db>'
        'LOCATION': "{}/{}".format(REDIS_URL, REDIS_DB),
        'OPTIONS': {
            # "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
            'PARSER_CLASS': 'redis.connection.HiredisParser',
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
        },
        'KEY_PREFIX': SESSION_REDIS_PREFIX,
        'TIMEOUT': 60 * 60 * 24 * 30  # 30 days
    },
    'db-cache': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'db_cache_table',
        'TIMEOUT': 30 * 60,
    },
}

RQ_QUEUES = {
    'default': {
        'URL': "{}/{}".format(REDIS_URL, 1),
        'DEFAULT_TIMEOUT': 360,
    },
}
