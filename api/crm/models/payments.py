"""Payment Models."""

# Django
from django.db import models

# Utils
from .utils import ApiModel

# Models
from .orders import Order, OrderItem
from .shippings import Shipping
from .products import Inventory
from .salesModule import SalesModule


class TypePayment(ApiModel):
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(max_length=300, blank=True, null=True)
    # percent
    is_tax_porcent = models.BooleanField(default=False)
    tax_porcent = models.FloatField(null=True, blank=True, default=0.0)
    # static values
    is_tax_static_value = models.BooleanField(default=False)
    tax_static_value = models.IntegerField(null=True, blank=True, default=0)

    is_cash = models.BooleanField(default=False)
    is_credit_card = models.BooleanField(default=False)
    is_debit_card = models.BooleanField(default=False)
    is_agreement = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Payments_type_payment'

    def __str__(self):
        return self.name


class Payment(ApiModel):
    type_payment = models.ForeignKey('TypePayment', related_name='type_payment', blank=False, null=True,
                                     on_delete=models.SET_NULL)
    sales_module = models.ForeignKey('SalesModule', related_name='sales_module_payment', blank=False, null=True,
                                     on_delete=models.SET_NULL)
    order = models.OneToOneField('Order', related_name='payment_order', on_delete=models.CASCADE, blank=False, null=False)
    # calculate value: amount_pay
    amount_pay = models.IntegerField(blank=False, null=False)
    amount_change = models.IntegerField(blank=True, null=True)
    amount_final = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.order)
