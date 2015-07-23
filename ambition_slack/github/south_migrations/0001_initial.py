# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
        ('slack', '0001_initial'),
    )

    def forwards(self, orm):
        # Adding model 'GithubUser'
        db.create_table(u'github_githubuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.TextField')()),
            ('username', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'github', ['GithubUser'])


    def backwards(self, orm):
        # Deleting model 'GithubUser'
        db.delete_table(u'github_githubuser')


    models = {
        u'github.githubuser': {
            'Meta': {'object_name': 'GithubUser'},
            'email': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['github']
