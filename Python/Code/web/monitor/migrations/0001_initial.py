# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tweet'
        db.create_table('monitor_tweet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tweet_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 6, 0, 0))),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('monitor', ['Tweet'])


    def backwards(self, orm):
        # Deleting model 'Tweet'
        db.delete_table('monitor_tweet')


    models = {
        'monitor.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 6, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'tweet_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['monitor']