from django.contrib import admin
from django.contrib.gis import admin as gisadmin

# Register your models here.
from models import ServiceProvider, ServiceArea


class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']


admin.site.register(ServiceProvider, ServiceProviderAdmin)
admin.site.register(ServiceArea, gisadmin.GeoModelAdmin)
