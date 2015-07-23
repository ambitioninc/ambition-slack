# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slack', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='GithubUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.TextField(unique=True)),
                ('slack_user', models.OneToOneField(to='slack.SlackUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
