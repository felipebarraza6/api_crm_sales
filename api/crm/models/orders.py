"""Order Models."""

# Python
import uuid

# Django
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Utils
from .utils import ApiModel

# Models
from .clients import Client
from .products import Product, Price
from .users import User
from .deliveries import Delivery


class Order(ApiModel):
    # Unique Code Base Uuid
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)

    # External Origin
    client = models.ForeignKey('Client', related_name='order_client', on_delete=models.CASCADE)
    user = models.ForeignKey('User', related_name='order_owner', on_delete=models.CASCADE)
    # Internal Origin
    # Notes
    note_order = models.TextField(max_length=250, blank=True, null=True)
    note_delivery = models.TextField(max_length=250, blank=True, null=True)
    # Total Amount
    total_amount = models.IntegerField(blank=True, null=True, default=0)
    total_with_taxts = models.IntegerField(blank=True, null=True, default=0)
    # Options Boolean: only option "is_active" is True in initial register
    is_paid = models.BooleanField(default=False)
    is_null = models.BooleanField(default=False)
    is_delivery = models.BooleanField(default=False)
    delivery = models.ForeignKey('Delivery', related_name='order_delivery_service', on_delete=models.CASCADE,
                                 blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.uuid)


class OrderItem(ApiModel):
    order = models.ForeignKey('Order', related_name='order_item', on_delete=models.CASCADE)
    product = models.ForeignKey('Price', related_name='item_product', on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)

    def delete(self, *args, **kwargs):
        # Order
        order = Order.objects.filter(uuid=self.order.uuid).first()
        old_value_total_amount = order.total_amount
        # Product
        product = Price.objects.filter(id=str(self.product.id)).first()
        value_price = product.price * self.quantity
        # Rest Value
        calculate = old_value_total_amount - value_price
        # Update Order
        Order.objects.filter(uuid=self.order.uuid).update(total_amount=calculate)
        # Deleting Item Order
        super(OrderItem, self).delete(*args, **kwargs)

    def __str__(self):
        return str(('Order:{} Product:{}: Quantiy:{}').format(self.order, self.product, self.quantity))

    class Meta:
        verbose_name_plural = 'Orders_items'
