# DRF
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

#Models
from api.crm.models import Client

#Filters
from django_filters import rest_framework as filters

#Serializers
from api.crm.serializers import ClientModelSerializer, ProfileModelSerializer


#Client View Set
class ClientViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin, 
                  mixins.UpdateModelMixin, 
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin):

    queryset = Client.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    lookup_field = 'phone_number'
    permission_classes = [IsAuthenticated]

    class ClientFilter(filters.FilterSet):
        class Meta:
            model = Client
            fields = {
                'dni': ['exact', 'contains'],
                'first_name': ['contains', 'exact'],
                'last_name': ['contains', 'exact'],
                'phone_number': ['contains', 'exact'],
                'email': ['contains', 'exact'],
                'is_active': ['exact'],
                'address_exact': ['contains', 'exact'],
                'created': [
                    'contains',
                    'gte',
                    'lte',
                    'year',
                    'month',
                    'day',
                    'year__range',
                    'month__range',
                    'day__range',
                    'date__range'
                ]
            }
    
    filterset_class = ClientFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProfileModelSerializer
        else:
            return ClientModelSerializer