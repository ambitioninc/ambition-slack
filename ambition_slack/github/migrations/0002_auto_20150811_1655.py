# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('github', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='githubuser',
            name='api_token',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='githubuser',
            name='slack_user',
            field=models.OneToOneField(related_name='github_user', to='slack.SlackUser'),
            preserve_default=True,
        ),
    ]
