import os
if os.environ.get('RQ_SETTINGS_FROM') == 'settings.development':
    from .development import *
else:
    from .production import *


import sentry_sdk
from sentry_sdk.integrations.rq import RqIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DNS', ''),
    integrations=[RqIntegration()]
)
