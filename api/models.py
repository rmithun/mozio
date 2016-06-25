from django.db import models
from django.contrib.gis.db import models as gismodels

# Create your models here.


class ServiceProvider(models.Model):

    """type of service providers"""

    email = models.EmailField(max_length=100, db_index=True)
    name = models.CharField(max_length=25)
    language = models.CharField(max_length=25)
    currency = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name


class ServiceArea(models.Model):

    """service area of ServiceProvider"""
    provider = models.ForeignKey(
        ServiceProvider, related_name='service_provider')
    polygon = gismodels.PolygonField(null=True)
    name = models.CharField(max_length=25)
    price = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now=True)
    objects = gismodels.GeoManager()
