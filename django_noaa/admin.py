from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from admin_steroids.queryset import ApproxCountQuerySet
from admin_steroids.utils import view_related_link

import models

class StationAdmin(admin.ModelAdmin):
    
    list_display = (
        'id',
        'wban',
        'country',
        'state',
        'location',
        'name',
        'vector',
        'status',
        'operation',
        'elevation',
        'latitude',
        'longitude',
        'network',
        'load_temperatures',
        'load_temperatures_min_date_loaded',
        'load_temperatures_max_date_loaded',
    )
    
    list_filter = (
        'load_temperatures',
        'state',
        'country',
        'status',
        'operation',
        'network',
    )
    
    search_fields = (
        'name',
        'location',
        #'state',
        #'country',
    )
    
    def temperature_link(self, obj=None):
        if not obj:
            return ''
        return view_related_link(obj, 'temperatures')
    temperature_link.allow_tags = True
    temperature_link.short_description = 'temperatures'
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def get_actions(self, request):
        actions = super(StationAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def get_readonly_fields(self, request, obj=None):
        exclude = ['load_temperatures', 'load_temperatures_min_year']
        return [f.name for f in self.model._meta.fields if f.name not in exclude] + ['temperature_link']
    
    def queryset(self, *args, **kwargs):
        qs = super(StationAdmin, self).queryset(*args, **kwargs)
        qs = qs._clone(klass=ApproxCountQuerySet)
        return qs

admin.site.register(
    models.Station,
    StationAdmin)

class TemperatureAdmin(admin.ModelAdmin):
    
    list_display = (
        'id',
        'station',
        'obs_start_datetime',
        'obs_end_datetime',
        
        't_min',
        't_hr_avg',
        't_max',
    )
    
    list_filter = (
        'obs_start_datetime',
        #'obs_start_datetime__year',
    )
    
    search_fields = (
        'station__location',
        'station__name',
    )
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def get_actions(self, request):
        actions = super(TemperatureAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
    
    def get_readonly_fields(self, request, obj=None):
        exclude = []
        return [f.name for f in self.model._meta.fields if f.name not in exclude]
    
    def queryset(self, *args, **kwargs):
        qs = super(TemperatureAdmin, self).queryset(*args, **kwargs)
        qs = qs._clone(klass=ApproxCountQuerySet)
        return qs

admin.site.register(
    models.Temperature,
    TemperatureAdmin)
