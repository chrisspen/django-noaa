# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Station.load_temperatures_min_year'
        db.add_column(u'django_noaa_station', 'load_temperatures_min_year',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Station.load_temperatures_min_date_loaded'
        db.add_column(u'django_noaa_station', 'load_temperatures_min_date_loaded',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Station.load_temperatures_max_date_loaded'
        db.add_column(u'django_noaa_station', 'load_temperatures_max_date_loaded',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Station.load_temperatures_min_year'
        db.delete_column(u'django_noaa_station', 'load_temperatures_min_year')

        # Deleting field 'Station.load_temperatures_min_date_loaded'
        db.delete_column(u'django_noaa_station', 'load_temperatures_min_date_loaded')

        # Deleting field 'Station.load_temperatures_max_date_loaded'
        db.delete_column(u'django_noaa_station', 'load_temperatures_max_date_loaded')


    models = {
        'django_noaa.station': {
            'Meta': {'ordering': "('wban', 'country', 'state', 'location')", 'unique_together': "(('wban', 'country', 'state', 'location'),)", 'object_name': 'Station'},
            'closing': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'commissioning': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'elevation': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'load_temperatures': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'load_temperatures_max_date_loaded': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'load_temperatures_min_date_loaded': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'load_temperatures_min_year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
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