"""Order Serializers. """

# Django REST Framework
from rest_framework import serializers

# Models
from api.crm.models import Order, Payment, OrderItem, Shipping, Price, Inventory

from .payments import PaymentModelSerializer
from .delivery import DeliveriesForProductRetrieve, DeliveriesModelSerializer


class CancelOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = (
            'uuid',
            'total_amount',
            'user',
            'client',
            'note_order',
            'note_delivery',
            'is_delivery',
            'delivery',
            'total_amount',
            'total_with_taxts'
        )

    def update(self, instance, validated_data):
        if instance.is_null:
            raise serializers.ValidationError('Esta orden ya esta anulada')
        if instance.is_paid:
            raise serializers.ValidationError('Esta orden tiene un pago, no es posible anularla')

        for field in validated_data:
            if Order._meta.get_field(field):
                setattr(instance, field, validated_data[field])

        instance.save()
        return instance


class CreateOrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = (
            "uuid",
            'user',
            'client',
            'note_order',
            'is_delivery',
            'delivery',
            'note_delivery'
        )

        read_only_fields = (
            'uuid',
            'total_amount',
            'is_active',
            'is_paid',
        )

    def validate(self, data):
        if 'is_delivery' in data and 'delivery' not in data:
            raise serializers.ValidationError('Debes seleccionar el servicio de delivery')

        if 'note_delivery' in data and 'delivery' not in data:
            raise serializers.ValidationError('El pedido debe ser delivery para ingresar una nota de delivery')

        if 'client' in data:
            if not data['client'].is_active:
                raise serializers.ValidationError('El cliente no esta activo')

        return data


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'uuid',
            'client',
            'note_order',
            'note_delivery',
            'delivery',
            'is_delivery'
        )
        read_only_fields = (
            'uuid',
            'is_delivery',
        )

    def update(self, instance, validated_data):

        if instance.is_paid or instance.is_null:
            raise serializers.ValidationError('El no puede modificarse una vez pagado o anulado')

        if instance.is_delivery is False:
            if 'note_delivery' in validated_data:
                raise serializers.ValidationError('Este pedido no es delivery')
            if 'delivery' in validated_data:
                raise serializers.ValidationError('Este pedido no es delivery')

        for field in validated_data:
            if Order._meta.get_field(field):
                setattr(instance, field, validated_data[field])

        instance.save()
        return instance


# Ortder Item
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

    def create(self, data):
        quantity = data['quantity']
        get_order = Order.objects.filter(id=data['order'].id).first()
        get_price = Price.objects.filter(id=data['product'].id).first()

        if quantity > Inventory.objects.filter(product=get_price.product).first().stock:
            raise serializers.ValidationError('Excede existencias en inventario')

        if get_order.is_active is not True:
            raise serializers.ValidationError('Solo puedes agregar items a pedidos activos')

        if get_order.is_delivery:
            if get_price.is_delivery is not True:
                raise serializers.ValidationError('Debes elegir valores de delivery para este pedido')
            elif get_order.delivery != get_price.delivery:
                raise serializers.ValidationError('El precio no corresponde al delivery correcto')

        elif get_price.is_delivery:
            raise serializers.ValidationError('Debes elegir valores de precio normal para este pedido')

        OrderItem.objects.create(
            order=data['order'],
            product=data['product'],
            quantity=data['quantity']
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
        price = instance.product.price
        ORDER_OBJ = Order.objects.filter(id=instance.order.id).first()

        if ORDER_OBJ.is_active is not True:
            raise serializers.ValidationError('Este pedido no esta activo')

        old_quantity = OrderItem.objects.filter(id=instance.id).first().quantity
        old_price = old_quantity * price
        total_amount_order = ORDER_OBJ.total_amount

        re_format_total = total_amount_order - old_price

        Order.objects.filter(id=instance.order.id).update(
            total_amount=re_format_total,
            total_with_taxts=re_format_total
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

    def update(self, instance, validated_data):
        is_done = instance.is_done
        if is_done is True:
            raise serializers.ValidationError('Este envio ya fue cerrado!')

        instance.is_done = validated_data['is_done']
        instance.date_time_done = validated_data['date_time_done']
        instance.save()
        return instance


class ReOpenShippingSeriualizer(serializers.ModelSerializer):
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
        qs = Shipping.objects.filter(order=order).first()
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
            'is_delivery',
            'delivery',
            'note_delivery',
            'items',
            'payments',
            'shipping',
            'is_active',
            'is_paid',
            'is_null'
        )
