# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Tweet.tweet_id'
        db.alter_column('monitor_tweet', 'tweet_id', self.gf('django.db.models.fields.BigIntegerField')())

    def backwards(self, orm):

        # Changing field 'Tweet.tweet_id'
        db.alter_column('monitor_tweet', 'tweet_id', self.gf('django.db.models.fields.IntegerField')())

    models = {
        'monitor.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 6, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'tweet_id': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['monitor']