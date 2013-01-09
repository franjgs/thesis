# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        db.execute("alter table ratings_story convert to character set utf8")

    def backwards(self, orm):
        db.execute("alter table ratings_story convert to character set latin1")

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
    symmetrical = True
