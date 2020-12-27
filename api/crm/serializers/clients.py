"""Clients Serializers. """

#Django REST Framework
from rest_framework import serializers

#Models
from api.crm.models import Client, Order

#Serializers
from .orders import OrderDetailSerializer, OrderModelSerializer




class ClientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Client
        fields = '__all__'


class ProfileModelSerializer(serializers.ModelSerializer):
    
    orders_actives = serializers.SerializerMethodField('get_orders_actives')
    orders_finish = serializers.SerializerMethodField('get_orders_finish')

    def get_orders_actives(self, client):
        qs = Order.objects.filter(client = client, is_active=True)
        serializer = OrderModelSerializer(instance=qs, many=True)
        return serializer.data

    def get_orders_finish(self, client):
        qs = Order.objects.filter(client = client, is_paid=True)
        serializer = OrderModelSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Client
        fields = (
            'dni',
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'region',
            'commune',
            'province',
            'address_exact',
            'is_active',
            'orders_actives',
            'orders_finish',
        )
        
        