import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.utils.datastructures import MultiValueDictKeyError

from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos import GEOSException
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route

from .serializers import ServiceProviderSerializer, ServiceAreaSerializer
from .models import ServiceProvider, ServiceArea
# Create your views here.


@require_http_methods(['POST'])
def get_access(request):
    """
    allows already registered providers to CRUD on services
    """
    data = eval(request.body)
    email = data['email']
    phone_number = data['phone_number']
    service_provider = get_object_or_404(
        ServiceProvider,
        email=email,
        phone_number=phone_number)
    if service_provider:
        data = {'name': service_provider.name,
                'currency': service_provider.currency}
        return HttpResponse(json.dumps(data))
    return HttpResponse(500)


class ProviderViewSet(viewsets.ModelViewSet):

    """Service provider viewset """
    serializer_class = ServiceProviderSerializer
    queryset = ServiceProvider.objects.all()

    def create(self, request):
        data = self.request.data
        email = data['email']
        name = data['name']
        phone_number = data['phone_number']
        language = data['language']
        currency = data['currency']

        # Check email exists already
        exists = ServiceProvider.objects.filter(email=email)
        if not exists:
            ServiceProvider.objects.create(
                email=email,
                name=name,
                phone_number=phone_number,
                language=language,
                currency=currency)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class ServiceAreaViewset(viewsets.ModelViewSet):

    """CRUD for service area"""
    serializer_class = ServiceAreaSerializer
    queryset = ServiceArea.objects.all()
    lookup_field = 'id'

    def create(self, request):
        data = self.request.data
        email = data['email']
        phone_number = data['phone_number']
        price = data['price']
        name = data['name']
        geojson = eval(data['geojson'])
        polygon = fromstr(str(geojson['features'][0]['geometry']))
        service_provider = ServiceProvider.objects.filter(
            email=email,
            phone_number=phone_number)
        try:
            if service_provider:
                new_service_area = ServiceArea(
                    provider=service_provider[0],
                    price=price,
                    name=name,
                    polygon=polygon)
                new_service_area.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except GEOSException:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @list_route(methods=['get'])
    def valid_areas(self, request):
        try:
            lat = request.GET['lat']
            lon = request.GET['long']
            queryset = ServiceArea.objects.filter(
                polygon__contains='POINT(%s %s)' % (lon, lat))
            #queryset = ServiceArea.objects.all()
            return Response(ServiceAreaSerializer(
                queryset, context={'request': self.request}, many=True).data)
        except MultiValueDictKeyError, KeyError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @list_route(methods=['get'])
    def get_areas_of_provider(self, request):
        try:
            email = request.GET['email']
            phone = request.GET['phone_number']
            service_provider = ServiceProvider.objects.filter(
                email=email,
                phone_number=phone)
            if service_provider:
                queryset = ServiceArea.objects.filter(
                    provider=service_provider)
                return Response(ServiceAreaSerializer(
                    queryset,
                    context={'request': self.request}, many=True).data)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except MultiValueDictKeyError, KeyError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @detail_route(methods=['put'])
    def delete_service(self, request, id=None):
        try:
            data = self.request.data
            email = data['email']
            phone = data['phone_number']
            service_id = data['id']
            service_provider = ServiceProvider.objects.filter(
                email=email,
                phone_number=phone)
            if service_provider:
                ServiceArea.objects.filter(
                    id=id).delete()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except MultiValueDictKeyError, KeyError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @detail_route(methods=['put'])
    def update_service(self, request, id=None):
        data = self.request.data
        email = data['email']
        phone_number = data['phone_number']
        price = data['price']
        name = data['name']
        service_id = data['service_id']
        geojson = eval(data['geojson'])
        polygon = fromstr(str(geojson['features'][0]['geometry']))
        service_provider = ServiceProvider.objects.filter(
            email=email,
            phone_number=phone_number)
        try:
            if service_provider:
                new_service_area = ServiceArea.objects.filter(
                    id=service_id).update(
                    price=price,
                    name=name,
                    polygon=polygon)
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except GEOSException:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def load_editor(request, id):
    service_provider = ServiceArea.objects.get(
        id=id)
    if service_provider:
        return render(
            request,
            'add_provider/define_service.html', {'area': service_provider})
    else:
        return render(
            request,
            'add_provider/define_service.html', {})
