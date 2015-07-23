# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SlackUser'
        db.create_table(u'slack_slackuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.TextField')()),
            ('username', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'slack', ['SlackUser'])


    def backwards(self, orm):
        # Deleting model 'SlackUser'
        db.delete_table(u'slack_slackuser')


    models = {
        u'slack.slackuser': {
            'Meta': {'object_name': 'SlackUser'},
            'email': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['slack']