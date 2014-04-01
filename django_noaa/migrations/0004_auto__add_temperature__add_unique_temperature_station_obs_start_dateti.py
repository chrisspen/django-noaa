# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Temperature'
        db.create_table(u'django_noaa_temperature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('station', self.gf('django.db.models.fields.related.ForeignKey')(related_name='temperatures', to=orm['django_noaa.Station'])),
            ('obs_start_datetime', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('obs_end_datetime', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('crx_vn', self.gf('django.db.models.fields.CharField')(max_length=6, db_index=True)),
            ('t_calc', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('t_hr_avg', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('t_max', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('t_min', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('p_calc', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('solarad', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('solarad_flag', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('solarad_max', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('solarad_max_flag', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('solarad_min', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('solarad_min_flag', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('sur_temp_type', self.gf('django.db.models.fields.CharField')(max_length=1, db_index=True)),
            ('sur_temp', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('sur_temp_flag', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('sur_temp_max', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('sur_temp_max_flag', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('sur_temp_min', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('sur_temp_min_flag', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('rh_hr_avg', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('rh_hr_avg_flag', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('soil_moisture_5', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('soil_moisture_10', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('soil_moisture_20', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('soil_moisture_50', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('soil_moisture_100', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('soil_temp_5', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('soil_temp_10', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('soil_temp_20', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('soil_temp_50', self.gf('django.db.models.fields.FloatField')(db_index=True)),
            ('soil_temp_100', self.gf('django.db.models.fields.FloatField')(db_index=True)),
        ))
        db.send_create_signal('django_noaa', ['Temperature'])

        # Adding unique constraint on 'Temperature', fields ['station', 'obs_start_datetime', 'obs_end_datetime']
        db.create_unique(u'django_noaa_temperature', ['station_id', 'obs_start_datetime', 'obs_end_datetime'])


    def backwards(self, orm):
        # Removing unique constraint on 'Temperature', fields ['station', 'obs_start_datetime', 'obs_end_datetime']
        db.delete_unique(u'django_noaa_temperature', ['station_id', 'obs_start_datetime', 'obs_end_datetime'])

        # Deleting model 'Temperature'
        db.delete_table(u'django_noaa_temperature')


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
        },
        'django_noaa.temperature': {
            'Meta': {'unique_together': "(('station', 'obs_start_datetime', 'obs_end_datetime'),)", 'object_name': 'Temperature'},
            'crx_vn': ('django.db.models.fields.CharField', [], {'max_length': '6', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'obs_end_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'obs_start_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'p_calc': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'rh_hr_avg': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'rh_hr_avg_flag': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'soil_moisture_10': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'soil_moisture_100': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'soil_moisture_20': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'soil_moisture_5': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'soil_moisture_50': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'soil_temp_10': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'soil_temp_100': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'soil_temp_20': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'soil_temp_5': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'soil_temp_50': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'solarad': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'solarad_flag': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'solarad_max': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'solarad_max_flag': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'solarad_min': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'solarad_min_flag': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'temperatures'", 'to': "orm['django_noaa.Station']"}),
            'sur_temp': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'sur_temp_flag': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'sur_temp_max': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'sur_temp_max_flag': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'sur_temp_min': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            'sur_temp_min_flag': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'sur_temp_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            't_calc': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            't_hr_avg': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            't_max': ('django.db.models.fields.FloatField', [], {'db_index': 'True'}),
            't_min': ('django.db.models.fields.FloatField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['django_noaa']