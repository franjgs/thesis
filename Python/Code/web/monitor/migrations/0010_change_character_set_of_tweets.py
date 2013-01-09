# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        db.execute("alter table monitor_tweet convert to character set utf8")

    def backwards(self, orm):
        db.execute("alter table monitor_tweet convert to character set latin1")

    models = {
        'monitor.stats': {
            'Meta': {'object_name': 'Stats'},
            'created_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 9, 0, 0)', 'db_index': 'True'}),
            'depressed_count_bagging': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'depressed_count_boosting': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'depressed_count_stacking': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'depressed_count_svm': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'not_depressed_count_bagging': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'not_depressed_count_boosting': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'not_depressed_count_stacking': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'not_depressed_count_svm': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'monitor.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 9, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_bagging': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'label_boosting': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'label_stacking': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'label_svm': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'tweet_id': ('django.db.models.fields.BigIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['monitor']
    symmetrical = True
