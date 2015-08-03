# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('slack', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='slackuser',
            name='time_zone',
            field=timezone_field.fields.TimeZoneField(default=b'US/Eastern'),
            preserve_default=True,
        ),
    ]
