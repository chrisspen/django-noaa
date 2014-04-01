# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Station'
        db.create_table(u'django_noaa_station', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wban', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=10, db_index=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=10, db_index=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('vector', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('elevation', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('commissioning', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('closing', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('operation', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('pairing', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=100, null=True, blank=True)),
            ('network', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('load_temperatures', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('django_noaa', ['Station'])

        # Adding unique constraint on 'Station', fields ['wban', 'country', 'state', 'location']
        db.create_unique(u'django_noaa_station', ['wban', 'country', 'state', 'location'])


    def backwards(self, orm):
        # Removing unique constraint on 'Station', fields ['wban', 'country', 'state', 'location']
        db.delete_unique(u'django_noaa_station', ['wban', 'country', 'state', 'location'])

        # Deleting model 'Station'
        db.delete_table(u'django_noaa_station')


    models = {
        'django_noaa.station': {
            'Meta': {'unique_together': "(('wban', 'country', 'state', 'location'),)", 'object_name': 'Station'},
            'closing': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'commissioning': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'elevation': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'load_temperatures': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'network': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'operation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'pairing': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'vector': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'wban': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        }
    }

    complete_apps = ['django_noaa']