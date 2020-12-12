"""Shipping Models."""

#Django
from django.db import models

#Utils
from .users import ApiModel
from .orders import Order
from .deliveries import Delivery


class Shipping(ApiModel):
    order = models.ForeignKey('Order', related_name='order_shipping', on_delete=models.CASCADE)
    delivery = models.ForeignKey('Delivery', related_name='delivery_shipping', on_delete=models.CASCADE)
    address = models.TextField(null=False, blank=False, max_length='200')
    note = models.TextField(null=True, blank=True, max_length='350')

    class Meta:
        verbose_name_plural = 'Orders_shipping'

    def __str__(self):
        return str(self.order.uuid)

