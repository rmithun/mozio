from rest_framework import serializers

from models import ServiceProvider, ServiceArea


class ServiceProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceProvider
        fields = ('email', 'name', 'phone_number', 'language', 'currency')


class ServiceAreaSerializer(serializers.ModelSerializer):
    provider = ServiceProviderSerializer()

    class Meta:
        model = ServiceArea
        fields = ('id', 'polygon', 'name', 'price', 'provider')
