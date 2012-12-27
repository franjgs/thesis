# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Story.ups'
        db.add_column('ratings_story', 'ups',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Story.downs'
        db.add_column('ratings_story', 'downs',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Story.ups'
        db.delete_column('ratings_story', 'ups')

        # Deleting field 'Story.downs'
        db.delete_column('ratings_story', 'downs')


    models = {
        'ratings.story': {
            'Meta': {'object_name': 'Story'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'downs': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id36': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'label': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ups': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['ratings']