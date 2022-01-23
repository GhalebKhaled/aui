from __future__ import unicode_literals

from .base import *

import dj_database_url


SECRET_KEY = os.environ['SECRET_KEY']

WSGI_APPLICATION = 'wsgi.heroku.application'

STUNNEL_ENABLED = False

CONFIGURED_ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')
for host in CONFIGURED_ALLOWED_HOSTS:
    if host:
        ALLOWED_HOSTS.append(host)

DATABASE_URL = os.environ.get('RDS_DATABASE_URL') or os.environ['DATABASE_URL']
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL),
}
if os.environ['ENABLE_AWS_RDS_SSL'] == 'True':
    DATABASES['default']['OPTIONS'] = {
        'sslmode': 'verify-full',
        'sslrootcert': 'certs/rds-combined-ca-bundle.pem',
    }
DATABASES['default']['CONN_MAX_AGE'] = None

STATICFILES_STORAGE = 'storage.NonPackagingS3PipelineCachedStorage'

DEFAULT_FILE_STORAGE = 'storage.MediaStorage'
MEDIA_URL = 'https://{}/media/'.format(AWS_S3_CUSTOM_DOMAIN)

ADMIN_MEDIA_PREFIX = ''.join([STATIC_URL, 'admin/'])

# djangosecure settings
SECURE_FRAME_DENY = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CACHES['default']['OPTIONS']['CONNECTION_POOL_KWARGS'] = {}
CACHES['session']['OPTIONS']['CONNECTION_POOL_KWARGS'] = {}
CACHES['rq-cache']['OPTIONS']['CONNECTION_POOL_KWARGS'] = {}
