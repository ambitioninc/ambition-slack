# This file was put together based on instructions from [0]
# [0] - http://celery.readthedocs.org/en/latest/django/first-steps-with-django.html
from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ambition_slack.settings')

app = Celery('ambition_slack')

# This allows us to configure directly from Django settings - see [0]
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
