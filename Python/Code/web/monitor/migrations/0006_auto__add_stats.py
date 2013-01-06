# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Stats'
        db.create_table('monitor_stats', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 1, 6, 0, 0), db_index=True)),
            ('depressed_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('happy_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('monitor', ['Stats'])


    def backwards(self, orm):
        # Deleting model 'Stats'
        db.delete_table('monitor_stats')


    models = {
        'monitor.stats': {
            'Meta': {'object_name': 'Stats'},
            'created_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 6, 0, 0)', 'db_index': 'True'}),
            'depressed_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'happy_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'monitor.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 6, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'tweet_id': ('django.db.models.fields.BigIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['monitor']