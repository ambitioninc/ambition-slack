# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slack', '0002_slackuser_time_zone'),
    ]

    operations = [
        migrations.AddField(
            model_name='slackuser',
            name='expects_morning_digest',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
