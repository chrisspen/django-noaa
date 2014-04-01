# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Station.elevation'
        db.alter_column(u'django_noaa_station', 'elevation', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'Station.wban'
        db.alter_column(u'django_noaa_station', 'wban', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Station.elevation'
        raise RuntimeError("Cannot reverse this migration. 'Station.elevation' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Station.elevation'
        db.alter_column(u'django_noaa_station', 'elevation', self.gf('django.db.models.fields.PositiveIntegerField')())

        # User chose to not deal with backwards NULL issues for 'Station.wban'
        raise RuntimeError("Cannot reverse this migration. 'Station.wban' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Station.wban'
        db.alter_column(u'django_noaa_station', 'wban', self.gf('django.db.models.fields.CharField')(max_length=100))

    models = {
        'django_noaa.station': {
            'Meta': {'unique_together': "(('wban', 'country', 'state', 'location'),)", 'object_name': 'Station'},
            'closing': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'commissioning': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'elevation': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
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
            'wban': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['django_noaa']