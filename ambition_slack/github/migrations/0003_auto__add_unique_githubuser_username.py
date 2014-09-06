# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'GithubUser', fields ['username']
        db.create_unique(u'github_githubuser', ['username'])


    def backwards(self, orm):
        # Removing unique constraint on 'GithubUser', fields ['username']
        db.delete_unique(u'github_githubuser', ['username'])


    models = {
        u'github.githubuser': {
            'Meta': {'object_name': 'GithubUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slack_user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['slack.SlackUser']", 'unique': 'True'}),
            'username': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        },
        u'slack.slackuser': {
            'Meta': {'object_name': 'SlackUser'},
            'email': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'username': ('django.db.models.fields.TextField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['github']