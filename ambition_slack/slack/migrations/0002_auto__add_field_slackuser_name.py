# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SlackUser.name'
        db.add_column(u'slack_slackuser', 'name',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SlackUser.name'
        db.delete_column(u'slack_slackuser', 'name')


    models = {
        u'slack.slackuser': {
            'Meta': {'object_name': 'SlackUser'},
            'email': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'username': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['slack']