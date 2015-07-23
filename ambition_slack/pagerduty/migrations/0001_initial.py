# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slack', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertReceipt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alert_type', models.CharField(max_length=128, choices=[(b'incident.trigger', b'Trigger'), (b'incident.resolve', b'Resolve')])),
                ('incident_uid', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PagerdutyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.TextField(unique=True)),
                ('slack_user', models.OneToOneField(to='slack.SlackUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='alertreceipt',
            unique_together=set([('alert_type', 'incident_uid')]),
        ),
    ]
