# DRF
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

# Models
from api.crm.models import Order, OrderItem, Shipping

# Filters
from django_filters import rest_framework as filters

# Serializers
from api.crm.serializers import OrderDetailSerializer, CreateOrderSerializer, UpdateOrderSerializer, \
    CancelOrderSerializer, AddItemSerializer, UpdateItemSerializer, ListDetailShippingSerializers, OrderModelSerializer, \
    ReOpenShippingSeriualizer

# Django
from django.utils import timezone


# Shipping
class ShippingViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin):
    queryset = Shipping.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    class ShippingFilter(filters.FilterSet):
        class Meta:
            model = Shipping
            fields = {
                'order': ['exact'],
                'created': ['contains', 'gte', 'lte', 'year', 'month', 'day', 'year__range', 'month__range',
                            'day__range', 'date__range'],
                'delivery': ['exact']
            }

    filterset_class = ShippingFilter

    def get_serializer_class(self):
        if self.action == 'finish':
            return ListDetailShippingSerializers
        if self.action == 're_open':
            return ReOpenShippingSeriualizer
        else:
            return ListDetailShippingSerializers

    @action(detail=True, methods=['post'])
    def finish(self, request, *args, **kwargs):
        module = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            module,
            data={'is_done': True, 'date_time_done': timezone.now()},
            context=self.get_serializer_context(),
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        module = serializer.save()
        data = ListDetailShippingSerializers(module).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def re_open(self, request, *args, **kwargs):
        module = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            module,
            data={'is_done': False, 'date_time_done': None},
            context=self.get_serializer_context(),
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        module = serializer.save()
        data = ListDetailShippingSerializers(module).data
        return Response(data, status=status.HTTP_200_OK)

        # Item ViewSet


class OrderItemViewSet(viewsets.GenericViewSet,
                       mixins.DestroyModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin):
    queryset = OrderItem.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    class OrderItemFilter(filters.FilterSet):
        class Meta:
            model = OrderItem
            fields = {
                'order': ['exact']
            }

    filterset_class = OrderItemFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return AddItemSerializer
        if self.action == 'partial_update':
            return UpdateItemSerializer


# Order ViewSet
class OrderViewSet(viewsets.GenericViewSet,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin):
    queryset = Order.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    lookup_field = 'uuid'
    permission_classes = [IsAuthenticated]

    class OrderFilter(filters.FilterSet):
        class Meta:
            model = Order
            fields = {
                'uuid': ['exact', 'contains'],
                'user': ['exact'],
                'client': ['exact'],
                'is_active': ['exact'],
                'is_paid': ['exact'],
                'is_delivery': ['exact'],
                'created': ['contains', 'gte', 'lte', 'year', 'month', 'day', 'year__range', 'month__range',
                            'day__range', 'date__range'],

            }

    filterset_class = OrderFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return OrderDetailSerializer
        if self.action == 'create':
            return CreateOrderSerializer
        if self.action == 'partial_update':
            return UpdateOrderSerializer
        if self.action == 'cancel_order':
            return CancelOrderSerializer

    @action(detail=True, methods=['post'])
    def cancel_order(self, request, *args, **kwargs):
        order = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            order,
            data={'is_active': False, 'is_paid': False, 'is_null': True},
            context=self.get_serializer_context(),
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        data = OrderModelSerializer(order).data
        return Response(data, status=status.HTTP_200_OK)
