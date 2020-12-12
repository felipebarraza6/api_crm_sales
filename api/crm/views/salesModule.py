# DRF
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Django
from django.utils import timezone

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

# Models
from api.crm.models import SalesModule

# Filters
from django_filters import rest_framework as filters

# Serializers
from api.crm.serializers import CreateSalesModuleSerializer, ListSalesModuleSerializer, RetrieveModuleSales, \
    FinishModuleSales


class SalesModuleViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin):
    queryset = SalesModule.objects.all().order_by('-created')
    filter_backends = (filters.DjangoFilterBackend,)
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    class SalesModuleFilter(filters.FilterSet):
        class Meta:
            model = SalesModule
            fields = {
                'user': ['exact'],
                'is_active': ['exact'],
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
                ],
                'date_finish': [
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

    filterset_class = SalesModuleFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ListSalesModuleSerializer
        if self.action == 'retrieve':
            return RetrieveModuleSales
        if self.action == 'finish':
            return FinishModuleSales
        else:
            return CreateSalesModuleSerializer

    @action(detail=True, methods=['post'])
    def finish(self, request, *args, **kwargs):
        module = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            module,
            data={'is_active': False, 'date_finish': timezone.now()},
            context=self.get_serializer_context(),
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        module = serializer.save()
        data = RetrieveModuleSales(module).data
        return Response(data, status=status.HTTP_200_OK)
