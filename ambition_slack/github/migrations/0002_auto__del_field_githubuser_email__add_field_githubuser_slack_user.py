# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'GithubUser.email'
        db.delete_column(u'github_githubuser', 'email')

        # Adding field 'GithubUser.slack_user'
        db.add_column(u'github_githubuser', 'slack_user',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=0, to=orm['slack.SlackUser'], unique=True),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'GithubUser.email'
        raise RuntimeError("Cannot reverse this migration. 'GithubUser.email' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'GithubUser.email'
        db.add_column(u'github_githubuser', 'email',
                      self.gf('django.db.models.fields.TextField')(),
                      keep_default=False)

        # Deleting field 'GithubUser.slack_user'
        db.delete_column(u'github_githubuser', 'slack_user_id')


    models = {
        u'github.githubuser': {
            'Meta': {'object_name': 'GithubUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slack_user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['slack.SlackUser']", 'unique': 'True'}),
            'username': ('django.db.models.fields.TextField', [], {})
        },
        u'slack.slackuser': {
            'Meta': {'object_name': 'SlackUser'},
            'email': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['github']