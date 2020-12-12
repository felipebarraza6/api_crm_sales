
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
from api.crm.models import Delivery

#Filters
from django_filters import rest_framework as filters

#Serializers
from api.crm.serializers import DeliveriesModelSerializer

class DeliveryViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin):
    
    queryset = Delivery.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    class DeliveryFilter(filters.FilterSet):
        class Meta:
            model = Delivery
            fields = {
                'name_service': ['contains']
            }

    filterset_class = DeliveryFilter
    serializer_class = DeliveriesModelSerializer

