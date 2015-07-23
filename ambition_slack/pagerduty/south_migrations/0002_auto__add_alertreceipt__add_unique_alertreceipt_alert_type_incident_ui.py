# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AlertReceipt'
        db.create_table(u'pagerduty_alertreceipt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alert_type', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('incident_uid', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'pagerduty', ['AlertReceipt'])

        # Adding unique constraint on 'AlertReceipt', fields ['alert_type', 'incident_uid']
        db.create_unique(u'pagerduty_alertreceipt', ['alert_type', 'incident_uid'])


    def backwards(self, orm):
        # Removing unique constraint on 'AlertReceipt', fields ['alert_type', 'incident_uid']
        db.delete_unique(u'pagerduty_alertreceipt', ['alert_type', 'incident_uid'])

        # Deleting model 'AlertReceipt'
        db.delete_table(u'pagerduty_alertreceipt')


    models = {
        u'pagerduty.alertreceipt': {
            'Meta': {'unique_together': "(('alert_type', 'incident_uid'),)", 'object_name': 'AlertReceipt'},
            'alert_type': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incident_uid': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
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