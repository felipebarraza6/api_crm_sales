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
from api.crm.models import Order, OrderItem, Shipping

#Filters
from django_filters import rest_framework as filters

#Serializers
from api.crm.serializers import OrderDetailSerializer, CreateOrderSerializer, UpdateOrderSerializer, OrderItemSerializer, AddItemSerializer, UpdateItemSerializer, ListDetailShippingSerializers


#Shipping
class ShippingViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin):
    
    queryset = Shipping.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    
    class ShippingFilter(filters.FilterSet):
        class Meta:
            model = Shipping
            fields = {
                'order': ['exact'],
                'created': ['contains', 'gte', 'lte', 'year', 'month', 'day', 'year__range', 'month__range', 'day__range', 'date__range'],   
            }
    
    filterset_class = ShippingFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ListDetailShippingSerializers        


#Item ViewSet
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
                'order':['exact']
            }
        
    filterset_class = OrderItemFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return AddItemSerializer
        if self.action == 'partial_update':
            return UpdateItemSerializer

#Order ViewSet
class OrderViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin, 
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin, 
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin):
    
    queryset = Order.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    lookup_field  = 'uuid'
    permission_classes = [IsAuthenticated]

    class OrderFilter(filters.FilterSet):
        class Meta:
            model = Order
            fields = {
                'uuid': ['exact'],
                'client': ['exact'],
                'is_active': ['exact'],
                'is_paid': ['exact'],
                'is_delivery': ['exact'],
                'created': ['contains', 'gte', 'lte', 'year', 'month', 'day', 'year__range', 'month__range', 'day__range', 'date__range'],   
                 
            }

    filterset_class = OrderFilter    


    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return OrderDetailSerializer                
        if self.action == 'create':
            return CreateOrderSerializer        
        if self.action == 'partial_update':
            return UpdateOrderSerializer