# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Story.subreddit'
        db.add_column('ratings_story', 'subreddit',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Story.subreddit'
        db.delete_column('ratings_story', 'subreddit')


    models = {
        'ratings.story': {
            'Meta': {'object_name': 'Story'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id36': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'label': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'subreddit': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['ratings']