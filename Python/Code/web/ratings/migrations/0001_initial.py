# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Story'
        db.create_table('ratings_story', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id36', self.gf('django.db.models.fields.CharField')(max_length=10, db_index=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('label', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('ratings', ['Story'])


    def backwards(self, orm):
        # Deleting model 'Story'
        db.delete_table('ratings_story')


    models = {
        'ratings.story': {
            'Meta': {'object_name': 'Story'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id36': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'label': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['ratings']