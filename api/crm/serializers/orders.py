"""Order Serializers. """

#Django REST Framework
from rest_framework import serializers

#Models
from api.crm.models import Order, Payment, OrderItem, Shipping

from .payments import PaymentModelSerializer
from .products import ProductDetailSerializer
from .delivery import DeliveriesForProductRetrieve, DeliveriesModelSerializer


class CreateOrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = (
            'user',
            'client',
            'note_order',            
            'is_delivery',
            'delivery',
            'note_delivery'
        )

        read_only = (
            'uuid',
            'total_amount',
            'is_active',
            'is_paid',            
        )
    
    def validate(self, data):
        if data['is_delivery'] == True and data['delivery'] is None:
            raise serializers.ValidationError('Debes seleccionar el servicio de delivery')
        if data['client'].is_active == False:
            raise serializers.ValidationError('El cliente no esta activo')
        return data

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (            
            'note_order',                     
            'note_delivery',
            'is_active',
            'delivery'
        )    
        
#Ortder Item
class OrderItemSerializer(serializers.ModelSerializer):
    
    order = serializers.StringRelatedField(many=False)

    class Meta:
        model = OrderItem
        fields = '__all__'

class AddItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'order',
            'product',
            'quantity'
        )
    
    def create(self,data):
        OrderItem.objects.create(
            order = data['order'],
            product = data['product'],
            quantity = data['quantity']
        )
        order_item = data['order'].id           
        old_value = Order.objects.filter(id = order_item).first().total_amount
        calculate = data['product'].price * data['quantity']
        Order.objects.filter(id=order_item).update(
            total_amount = calculate + old_value            
        )
        return data

class UpdateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'id',
            'quantity',
        )
    
    def update(self, instance, validated_data):                    

        old_value = instance.quantity * instance.product.price
        new_value = validated_data['quantity'] * instance.product.price

        old_value_order = Order.objects.filter(id=instance.order.id).first().total_amount

        Order.objects.filter(id=instance.order.id).update(
            total_amount = (old_value_order - old_value) + new_value
        )

        instance.quantity = validated_data['quantity']
        instance.save()
        
        return instance

class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class ListDetailShippingSerializers(serializers.ModelSerializer):
    delivery = DeliveriesForProductRetrieve()
    order = OrderModelSerializer()    
    class Meta:
        model = Shipping
        fields = '__all__'

class ShippingModelSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Shipping
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):

    payments = serializers.SerializerMethodField('get_payments')
    client = serializers.StringRelatedField(many=False)
    items = serializers.SerializerMethodField('get_order_items')
    shipping = serializers.SerializerMethodField('get_shippings')
    delivery = DeliveriesModelSerializer()

    def get_shippings(self, order):
        qs = Shipping.objects.filter(order = order).first()
        serializer = ShippingModelSerializer(instance=qs, many=False)
        return serializer.data

    def get_payments(self, order):
        qs = Payment.objects.filter(order=order)
        serializer = PaymentModelSerializer(instance=qs, many=True)
        return serializer.data

    def get_order_items(self, order):
        qs = OrderItem.objects.filter(order=order)
        serializer = OrderItemSerializer(instance=qs, many=True)
        return serializer.data    

    class Meta:
        model = Order
        fields = (
            'id',
            'uuid',
            'created',
            'client',
            'note_order',            
            'total_amount',
            'total_with_taxts',
            'is_active',
            'is_paid',
            'is_delivery',
            'delivery',
            'note_delivery',
            'items',
            'payments',
            'shipping'
        )


        