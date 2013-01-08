# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Stats.happy_count_boosting'
        db.delete_column('monitor_stats', 'happy_count_boosting')

        # Deleting field 'Stats.happy_count_svm'
        db.delete_column('monitor_stats', 'happy_count_svm')

        # Deleting field 'Stats.happy_count_stacking'
        db.delete_column('monitor_stats', 'happy_count_stacking')

        # Deleting field 'Stats.happy_count_bagging'
        db.delete_column('monitor_stats', 'happy_count_bagging')

        # Adding field 'Stats.not_depressed_count_svm'
        db.add_column('monitor_stats', 'not_depressed_count_svm',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Stats.not_depressed_count_bagging'
        db.add_column('monitor_stats', 'not_depressed_count_bagging',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Stats.not_depressed_count_boosting'
        db.add_column('monitor_stats', 'not_depressed_count_boosting',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Stats.not_depressed_count_stacking'
        db.add_column('monitor_stats', 'not_depressed_count_stacking',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Stats.happy_count_boosting'
        db.add_column('monitor_stats', 'happy_count_boosting',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Stats.happy_count_svm'
        db.add_column('monitor_stats', 'happy_count_svm',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Stats.happy_count_stacking'
        db.add_column('monitor_stats', 'happy_count_stacking',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Stats.happy_count_bagging'
        db.add_column('monitor_stats', 'happy_count_bagging',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Stats.not_depressed_count_svm'
        db.delete_column('monitor_stats', 'not_depressed_count_svm')

        # Deleting field 'Stats.not_depressed_count_bagging'
        db.delete_column('monitor_stats', 'not_depressed_count_bagging')

        # Deleting field 'Stats.not_depressed_count_boosting'
        db.delete_column('monitor_stats', 'not_depressed_count_boosting')

        # Deleting field 'Stats.not_depressed_count_stacking'
        db.delete_column('monitor_stats', 'not_depressed_count_stacking')


    models = {
        'monitor.stats': {
            'Meta': {'object_name': 'Stats'},
            'created_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 8, 0, 0)', 'db_index': 'True'}),
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 8, 0, 0)'}),
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