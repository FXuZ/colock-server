# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'user_manage_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cid', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('ukey', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('region_num', self.gf('django.db.models.fields.IntegerField')()),
            ('phone_num', self.gf('django.db.models.fields.BigIntegerField')()),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('reg_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'user_manage', ['User'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'user_manage_user')


    models = {
        u'user_manage.user': {
            'Meta': {'object_name': 'User'},
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'phone_num': ('django.db.models.fields.BigIntegerField', [], {}),
            'reg_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'region_num': ('django.db.models.fields.IntegerField', [], {}),
            'ukey': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['user_manage']