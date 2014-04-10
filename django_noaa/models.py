import csv
import os
import sys
import zipfile
import urllib2
from datetime import date, timedelta

import dateutil.parser

from pytz import UTC

from django.db import models, transaction
from django.db.models import Min, Max
from django.db.transaction import commit_on_success
from django.conf import settings
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils import timezone

import fixed2csv

try:
    from admin_steroids.utils import StringWithTitle
    APP_LABEL = StringWithTitle('django_noaa', 'NOAA')
except ImportError:
    APP_LABEL = 'django_noaa'

import settings as _settings
import constants as c

STATIONS_V1_KEYS = set([
    'STATUS', 'ELEVATION', 'NAME', 'COUNTRY', 'PAIRING', 'LONGITUDE',
    'COMMISSIONING', 'STATE', 'VECTOR', 'LOCATION', 'WBAN', 'LATITUDE',
    'CLOSING', 'OPERATION', 'NETWORK',
])

REFERENCE_DIR = os.path.abspath(os.path.join(os.path.split(__file__)[0], 'reference'))

def to_fahrenheit(deg):
    return 9.0/5.0*(deg)+32.0

class Station(models.Model):
    """
    Represents a NOAA weather station.
    """
    
    wban = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_index=True,
        editable=False,
        unique=False)
    
    country = models.CharField(
        max_length=10,
        blank=False,
        null=False,
        db_index=True,
        editable=False,
        unique=False)
    
    state = models.CharField(
        max_length=10,
        blank=False,
        null=False,
        db_index=True,
        editable=False,
        unique=False)
    
    location = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        db_index=True,
        editable=False,
        unique=False)
    
    vector = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        db_index=True,
        editable=False,
        unique=False)
    
    name = models.CharField(
        max_length=500,
        blank=False,
        null=False,
        editable=False,
        unique=False)
    
    latitude = models.FloatField(
        blank=False,
        db_index=True,
        editable=False,
        null=False)
    
    longitude = models.FloatField(
        blank=False,
        db_index=True,
        editable=False,
        null=False)
    
    elevation = models.PositiveIntegerField(
        blank=True,
        null=True,
        db_index=True,
        editable=False)
    
    status = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        editable=False,
        db_index=True)
    
    commissioning = models.DateTimeField(
        blank=True,
        null=True,
        editable=False,
        db_index=True)
    
    closing = models.DateTimeField(
        blank=True,
        null=True,
        editable=False,
        db_index=True)
    
    operation = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        editable=False,
        db_index=True)
    
    #WBAN of a related station?
    pairing = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        editable=False,
        db_index=True)
    
    network = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        editable=False,
        db_index=True)
    
    load_temperatures = models.BooleanField(
        default=False,
        db_index=True,
        help_text=_('If checked, historical hourly temperature data will be loaded for this station.'))
    
    load_temperatures_min_year = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text=_('The earliest year to load hourly temperature data. If none, defaults to the current year.'))
    
    load_temperatures_min_date_loaded = models.DateField(
        blank=True,
        null=True,
        editable=False,
        verbose_name=_('min date loaded'),
        help_text=_('The earliest date of hourly temperature data loaded.'))
    
    load_temperatures_max_date_loaded = models.DateField(
        blank=True,
        null=True,
        editable=False,
        verbose_name=_('max date loaded'),
        help_text=_('The latest date of hourly temperature data loaded.'))
    
    class Meta:
        app_label = APP_LABEL
        unique_together = (
            ('wban', 'country', 'state', 'location'),
        )
        ordering = (
            'wban', 'country', 'state', 'location',
        )
        
    natural_keys = ('wban', 'country', 'state', 'location')
    
    def natural_key(self):
        return (self.wban, self.country, self.state, self.location)
    
    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        
        if self.id:
            aggs = self.temperatures.all().aggregate(Min('obs_start_datetime'), Max('obs_start_datetime'))
            self.load_temperatures_min_date_loaded = aggs['obs_start_datetime__min']
            self.load_temperatures_max_date_loaded = aggs['obs_start_datetime__max']
        
        super(Station, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        url = settings.NOAA_STATIONS_URL
        print url
        lines = list(csv.DictReader(urllib2.urlopen(url).readlines(), delimiter='\t'))
        format_validated = False
        total = len(lines)
        i = 0
        for line in lines:
            i += 1
            print '\r%i of %i %.02f%%' % (i, total, i/float(total)*100),
            sys.stdout.flush()
            
            # Validate file format from the headers.
            if not format_validated:
                keys = set(line.keys())
                if keys == STATIONS_V1_KEYS:
                    format_validated = True
                else:
                    raise Exception, \
                        'Unknown file format headers. This may indicate a '\
                        'revised format that is not yet supported.'
            
            # Pre-process some fields.
            if line['ELEVATION'].strip() in ('UN', 'NA'):
                line['ELEVATION'] = None
            if line['WBAN'].strip() in ('UN', 'NA'):
                line['WBAN'] = None
            if line['CLOSING'].strip():
                line['CLOSING'] = dateutil.parser.parse(line['CLOSING'])
                if timezone.is_naive(line['CLOSING']):
                    line['CLOSING'] = line['CLOSING'].replace(tzinfo=UTC)
            else:
                line['CLOSING'] = None
            if line['COMMISSIONING'].strip():
                line['COMMISSIONING'] = dateutil.parser.parse(line['COMMISSIONING'])
                if timezone.is_naive(line['COMMISSIONING']):
                    line['COMMISSIONING'] = line['COMMISSIONING'].replace(tzinfo=UTC)
            else:
                line['COMMISSIONING'] = None
            
            # Calculate unique key.
            key = dict([(_.lower(), line[_.upper()]) for _ in cls.natural_keys])
            #print key
            #print line
            
            # Create or update record.
            if cls.objects.filter(**key).exists():
                # Update existing.
                cls.objects.filter(**key).update(**dict(
                    (_k.lower(), _v)
                    for _k, _v in line.iteritems()
                    if _k.lower() not in key
                ))
            else:
                # Create new.
                obj = cls(**dict(
                    (_k.lower(), _v)
                    for _k, _v in line.iteritems()
                ))
                obj.save()
        print
        print 'Done.'
    
    def load_temperature_records(self, force=False, year=0):
        """
        Loads temperature records for all years starting with the minimum year.
        """
        _year = year
        year = year or self.load_temperatures_min_year or date.today().year
        if not force and self.load_temperatures_max_date_loaded:
            year = max(year, self.load_temperatures_max_date_loaded.year)
        while year <= date.today().year:
            print 'year:',year
            self.load_temperature_records_for_year(year=year)
            year += 1
            if _year:
                break
        self.save()
        
    @commit_on_success
    def load_temperature_records_for_year(self, year):
        """
        Loads hourly temperature data from
        http://www1.ncdc.noaa.gov/pub/data/uscrn/products/hourly02/README.txt
        """
        print 'Loading hourly temperature recordings for year %i from station %s.' % (year, self.wban)
        url = settings.NOAA_HOURLY_TEMPERATURE_URL.format(
            file_format=3,
            year=year,
            state=self.state,
            location=self.location,
            vector=self.vector.replace(' ','_'))
#        print url
        #print REFERENCE_DIR
        #data = urllib2.urlopen(url).read()
        schema_fn = os.path.join(REFERENCE_DIR, 'USCRN_HOURLY0203.csv')
#        print schema_fn
        parser = fixed2csv.Schema(
            fn=schema_fn,
            name_field='name',
            length_field='length',
            help_field='description',
            type_field='type',
            delimiter=' ',#Why would anyone design a fixed-width format AND use a delimiter?!
        )
        data = urllib2.urlopen(url).read()
        lines = data.split('\n')
        total = data.count('\n') + 1
        i = 0
        for line in parser.open(fn=lines):
            i += 1
            try:
                if i == 1 or not i % 10:
                    print '\r%i of %i %.02f%%' % (i, total, i/float(total)*100),
                    sys.stdout.flush()
                
                # Skip blank lines.
                if line['utc_date'] is None:
                    continue
                
                # Cleanup utc_datetime.
                utc_datetime = dateutil.parser.parse(line['utc_date']+' '+line['utc_time'])
    #            print 'utc_datetime;',utc_datetime
                #line['utc_datetime'] = utc_datetime
                del line['utc_date']
                del line['utc_time']
                # utc_datetime is the end of the observed hour, so the 00 hour
                # belongs with the previous day's observation, since it contains
                # observations.
                line['obs_start_datetime'] = (utc_datetime - timedelta(hours=1)).replace(tzinfo=UTC)
                line['obs_end_datetime'] = utc_datetime.replace(tzinfo=UTC)
                
                # Throw away redundant local timestamps.
                del line['lst_date']
                del line['lst_time']
                
                # Throw away redundant lat/long coordinates.
                del line['latitude']
                del line['longitude']
                
                # Lookup station from wbanno.
                station = Station.objects.get(wban=line['wbanno'])
                line['station'] = station
                del line['wbanno']
                
                key = dict((_, line[_]) for _ in Temperature.natural_keys)
                if Temperature.objects.filter(**key).exists():
                    Temperature.objects.filter(**key).update(**line)
                else:
                    Temperature.objects.create(**line)
            except Exception, e:
                print>>sys.stderr, 'Unable to load line %i: %s' % (i, e)
                for k,v in sorted(line.iteritems(), key=lambda o:o[0]):
                    print>>sys.stderr, k,v
                raise

        print '\r%i of %i %.02f%%' % (total, total, 100),
        sys.stdout.flush()

class Temperature(models.Model):
    """
    Stores temperature data corresponding to the hourly02 measurement schema
    defined at:
    http://www1.ncdc.noaa.gov/pub/data/uscrn/products/hourly02/README.txt
    """

#    wbanno = models.CharField(
#        blank=True,
#        null=True,
#        editable=False,
#        db_index=True,
#        max_length=5,
#        help_text=_("The station WBAN number."))

    station = models.ForeignKey('Station', related_name='temperatures')
    
    obs_start_datetime = models.DateTimeField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("""Inclusive. The UTC datetime when recording began."""))

    obs_end_datetime = models.DateTimeField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("""Exclusive. The UTC datetime when the recording ended."""))

    natural_keys = ('station', 'obs_start_datetime', 'obs_end_datetime')

#    utc_time = models.CharField(
#        blank=False,
#        null=False,
#        editable=False,
#        db_index=True,
#        max_length=4,
#        help_text=_("The UTC time of the observation. "))

    # Unnecessary. Just use utc_datetime/obs_end_datetime.
#    lst_datetime = models.DateTimeField(
#        blank=False,
#        null=False,
#        editable=False,
#        db_index=True,
#        help_text=_("""The Local Standard Time (LST) date of the observation.
#            The Local Standard Time (LST) time of the observation.
#            Time is the end of the observed hour."""))

#    lst_time = models.CharField(
#        blank=False,
#        null=False,
#        editable=False,
#        db_index=True,
#        max_length=4,
#        help_text=_(""))

    crx_vn = models.CharField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        max_length=6,
        help_text=_("The version number of the station datalogger program that was in effect at the time of the observation. Note: should be treated as a string."))

    #These are duplicated in the station model.
#    longitude = models.FloatField(
#        blank=False,
#        null=False,
#        editable=False,
#        db_index=True,
#        help_text=_("Station longitude, using WGS-84."))
#
#    latitude = models.FloatField(
#        blank=False,
#        null=False,
#        editable=False,
#        db_index=True,
#        help_text=_("Station latitude, using WGS-84."))

    t_calc = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("""Average temperature, in degrees C, during the last 5 minutes of the hour.
            Note: USCRN/USRCRN stations have multiple co-located temperature sensors that record independent measurements.
            This value is a single temperature number that is calculated from the multiple independent measurements."""))

    t_hr_avg = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        verbose_name=_('mean temperature'),
        help_text=_("""Average temperature, in degrees C, during the entire hour.
            Note: USCRN/USRCRN stations have multiple co-located temperature sensors that record independent measurements.
            This value is a single temperature number that is calculated from the multiple independent measurements."""))

    t_max = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        verbose_name=_('maximum temperature'),
        help_text=_("Maximum temperature, in degrees C, during the hour.  Note: USCRN/USRCRN stations have multiple co-located temperature sensors that record independent measurements. This value is a single temperature number that is calculated from the multiple independent measurements. The independent measurements are the maximum for each sensor of 5-minute average temperatures measured every 10 seconds during the hour."))

    t_min = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        verbose_name=_('minimum temperature'),
        help_text=_("Minimum temperature, in degrees C, during the hour.  Note: USCRN/USRCRN stations have multiple co-located temperature sensors that record independent measurements. This value is a single temperature number that is calculated from the multiple independent measurements. The independent measurements are the mminimum for each sensor of 5-minute average temperatures measured every 10 seconds during the hour."))

    p_calc = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("Total amount of precipitation, in mm, recorded during the hour. Note: USCRN/USRCRN stations have multiple independent measures of precipitation; this P_CALC value is a single precipitation number that is calculated from the multiple independent measurements."))

    solarad = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("Average global solar radiation, in watts/meter^2, for the hour."))

    solarad_flag = models.IntegerField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("QC flag for average global solar radiation.  0 means good, 3 means erroneous."))

    solarad_max = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("Maximum global solar radiation, in watts/meter^2, for the hour."))

    solarad_max_flag = models.IntegerField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("QC flag for maximum global solar radiation.  0 means good, 3 means erroneous."))

    solarad_min = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("Minimum global solar radiation, in watts/meter^2, for the hour."))

    solarad_min_flag = models.IntegerField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("QC flag for minimum global solar radiation.  0 means good, 3 means erroneous."))

    sur_temp_type = models.CharField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        max_length=1,
        help_text=_("Type of surface tempearture measurement. 'R' to denote raw surface temperature measurements, 'C' to denote corrected surface temperature measurements, and 'U' when unknown."))

    sur_temp = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("Average surface temperature, in degrees C, for the hour."))

    sur_temp_flag = models.IntegerField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("QC flag for surface temperature.  0 means good, 3 means erroneous."))

    sur_temp_max = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("Maximum surface temperature, in degrees C, for the hour."))

    sur_temp_max_flag = models.IntegerField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("QC flag for surface temperature maximum.  0 means good, 3 means erroneous."))

    sur_temp_min = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("Minimum surface temperature, in degrees C, for the hour."))

    sur_temp_min_flag = models.IntegerField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("QC flag for surface temperature minimum.  0 means good, 3 means erroneous."))

    rh_hr_avg = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("RH average for hour."))

    rh_hr_avg_flag = models.IntegerField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("QC flag for RH average.  0 means good, 3 means erroneous."))

    soil_moisture_5 = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("Average soil moisture (volumetric water content) during the entire hour at 5 cm below the surface, the ratio of water volume over sample volume. Note: USCRN/USRCRN stations have multiple co-located moisture sensors that record independent measurements. This value is a single moisture number that is calculated from the multiple independent measurements."))

    soil_moisture_10 = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("Average soil moisture (volumetric water content) during the entire hour at 10 cm below the surface, the ratio of water volume over sample volume. Note: USCRN/USRCRN stations have multiple co-located moisture sensors that record independent measurements. This value is a single moisture number that is calculated from the multiple independent measurements."))

    soil_moisture_20 = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("Average soil moisture (volumetric water content) during the entire hour at 20 cm below the surface, the ratio of water volume over sample volume. Note: USCRN/USRCRN stations have multiple co-located moisture sensors that record independent measurements. This value is a single moisture number that is calculated from the multiple independent measurements."))

    soil_moisture_50 = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("Average soil moisture (volumetric water content) during the entire hour at 50 cm below the surface, the ratio of water volume over sample volume. Note: USCRN/USRCRN stations have multiple co-located moisture sensors that record independent measurements. This value is a single moisture number that is calculated from the multiple independent measurements."))

    soil_moisture_100 = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("Average soil moisture (volumetric water content) during the entire hour at 100 cm below the surface, the ratio of water volume over sample volume. Note: USCRN/USRCRN stations have multiple co-located moisture sensors that record independent measurements. This value is a single moisture number that is calculated from the multiple independent measurements."))

    soil_temp_5 = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("Average soil temperature during the entire hour at 5 cm below the surface, in degrees C. Note: USCRN/USRCRN stations have multiple co-located temperature sensors that record independent measurements. This value is a single temperature number that is calculated from the multiple independent measurements."))

    soil_temp_10 = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("Average soil temperature during the entire hour at 10 cm below the surface, in degrees C. Note: USCRN/USRCRN stations have multiple co-located temperature sensors that record independent measurements. This value is a single temperature number that is calculated from the multiple independent measurements."))

    soil_temp_20 = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("Average soil temperature during the entire hour at 20 cm below the surface, in degrees C. Note: USCRN/USRCRN stations have multiple co-located temperature sensors that record independent measurements. This value is a single temperature number that is calculated from the multiple independent measurements."))

    soil_temp_50 = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("Average soil temperature during the entire hour at 50 cm below the surface, in degrees C. Note: USCRN/USRCRN stations have multiple co-located temperature sensors that record independent measurements. This value is a single temperature number that is calculated from the multiple independent measurements."))

    soil_temp_100 = models.FloatField(
        blank=False,
        null=False,
        editable=False,
        db_index=True,
        help_text=_("Average soil temperature during the entire hour at 100 cm below the surface"))

    class Meta:
        app_label = APP_LABEL
        unique_together = (
            ('station', 'obs_start_datetime', 'obs_end_datetime'),
        )
        
    def __unicode__(self):
        return u'%s:%s-%s' % (self.station.wban, self.obs_start_datetime, self.obs_end_datetime)
