# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'SlackUser', fields ['username']
        db.create_unique(u'slack_slackuser', ['username'])

        # Adding unique constraint on 'SlackUser', fields ['email']
        db.create_unique(u'slack_slackuser', ['email'])


    def backwards(self, orm):
        # Removing unique constraint on 'SlackUser', fields ['email']
        db.delete_unique(u'slack_slackuser', ['email'])

        # Removing unique constraint on 'SlackUser', fields ['username']
        db.delete_unique(u'slack_slackuser', ['username'])


    models = {
        u'slack.slackuser': {
            'Meta': {'object_name': 'SlackUser'},
            'email': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'username': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['slack']