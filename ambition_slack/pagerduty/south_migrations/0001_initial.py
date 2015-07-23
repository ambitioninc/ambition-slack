# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PagerdutyUser'
        db.create_table(u'pagerduty_pagerdutyuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slack_user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['slack.SlackUser'], unique=True)),
            ('email', self.gf('django.db.models.fields.TextField')(unique=True)),
        ))
        db.send_create_signal(u'pagerduty', ['PagerdutyUser'])


    def backwards(self, orm):
        # Deleting model 'PagerdutyUser'
        db.delete_table(u'pagerduty_pagerdutyuser')


    models = {
        u'pagerduty.pagerdutyuser': {
            'Meta': {'object_name': 'PagerdutyUser'},
            'email': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slack_user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['slack.SlackUser']", 'unique': 'True'})
        },
        u'slack.slackuser': {
            'Meta': {'object_name': 'SlackUser'},
            'email': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'username': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['pagerduty']