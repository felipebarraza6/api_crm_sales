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
from api.crm.models import Config

#Filters
from django_filters import rest_framework as filters

#Serializers
from api.crm.serializers import ConfigModelSerializer


class ConfigViewSet(viewsets.GenericViewSet):    
    
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Config.objects.all().first()
        serializer = ConfigModelSerializer(queryset, many=False)
        return Response(serializer.data)