# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Story.content'
        db.alter_column('ratings_story', 'content', self.gf('django.db.models.fields.CharField')(max_length=1000))

    def backwards(self, orm):

        # Changing field 'Story.content'
        db.alter_column('ratings_story', 'content', self.gf('django.db.models.fields.CharField')(max_length=500))

    models = {
        'ratings.story': {
            'Meta': {'object_name': 'Story'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id36': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'label': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'subreddit': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['ratings']