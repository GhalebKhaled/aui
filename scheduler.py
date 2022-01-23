from __future__ import unicode_literals

import datetime
from collections import defaultdict
import logging
from django.conf import settings

import django_rq


logger = logging.getLogger(__name__)


def schedule_once(interval, func, timeout=None):
    """
    Schedule job once or reschedule when interval changes
    """
    rq_scheduler = django_rq.get_scheduler('default')
    jobs = list(rq_scheduler.get_jobs())

    functions = defaultdict(lambda: list())
    for job in jobs:
        functions[job.func] = [job.meta.get('interval'), job.timeout, ]

    if not timeout:
        timeout = settings.RQ_QUEUES.get('DEFAULT_TIMEOUT', 360)

    if func not in functions or interval not in functions[func] or functions[func][1] != timeout or len(functions[func]) > 2:
        logger.info('Rescheduling job {} with interval: {}s'.format(func.__name__, interval))
        # clear all scheduled jobs for this function
        map(rq_scheduler.cancel, filter(lambda x: x.func==func, jobs))

        # schedule with new interval and timeout
        rq_scheduler.schedule(datetime.datetime.now(), func, interval=interval, timeout=timeout)
    else:
        logger.info('Job already scheduled every {}s: {}'.format(interval, func.__name__))
