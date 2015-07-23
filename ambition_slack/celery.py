# This file was put together based on instructions from [0]
# [0] - http://celery.readthedocs.org/en/latest/django/first-steps-with-django.html
from __future__ import absolute_import

import os

from celery import Celery
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('ambition_slack')

# This allows us to configure directly from Django settings - see [0]
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@periodic_task(run_every=(crontab(hour="20", minute="0,15,20,30", day_of_week="1,2,3,4,5")), ignore_result=True)
def this_is_a_test():
    EmailMultiAlternatives('Celery test', 'This is a test', '', ['joshmarlow@gmail.com']).send()
