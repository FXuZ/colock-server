# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Message'
        db.create_table(u'message_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender_uid', self.gf('django.db.models.fields.IntegerField')()),
            ('receiver_uid', self.gf('django.db.models.fields.IntegerField')()),
            ('message_key', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('send_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('img', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'message', ['Message'])


    def backwards(self, orm):
        # Deleting model 'Message'
        db.delete_table(u'message_message')


    models = {
        u'message.message': {
            'Meta': {'ordering': "('receiver_uid',)", 'object_name': 'Message'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'message_key': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'receiver_uid': ('django.db.models.fields.IntegerField', [], {}),
            'send_time': ('django.db.models.fields.DateTimeField', [], {}),
            'sender_uid': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['message']