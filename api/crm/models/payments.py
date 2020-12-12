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

    class Meta:
        verbose_name = 'Payments_type_payment'

    def __str__(self):
        return self.name


class Payment(ApiModel):
    type_payment = models.ForeignKey('TypePayment', related_name='type_pyment', blank=False, null=False,
                                     on_delete=models.CASCADE)
    sales_module = models.ForeignKey('SalesModule', related_name='sales_module_payment', blank=False, null=False,
                                     on_delete=models.PROTECT)
    order = models.ForeignKey('Order', related_name='payment_order', on_delete=models.PROTECT, blank=False, null=False)
    # calculate value: amount_pay
    amount_pay = models.IntegerField(blank=False, null=False)
    amount_change = models.IntegerField(blank=True, null=True)
    amount_final = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        get_order = Order.objects.filter(uuid=self.order.uuid).first()
        order_total_amount = get_order.total_amount

        amount_deli = get_order.total_amount
        if (get_order.is_delivery == True):
            shipping = Shipping(
                order=self.order,
                delivery=self.order.delivery,
                address=self.order.client.address_exact,
                note=self.order.note_delivery
            )
            shipping.save()

            delivery = get_order.delivery
            amount_deli = 0
            if delivery.is_tax_porcent == True:
                amount_deli += (order_total_amount * delivery.tax_porcent)

            elif delivery.is_tax_static_value == True:
                amount_deli += delivery.tax_static_value

        type_payment = self.type_payment
        type_payment_amount = 0
        if type_payment.is_tax_porcent:
            type_payment_amount += (order_total_amount * type_payment.tax_porcent)
        elif type_payment.is_tax_static_value:
            type_payment_amount += type_payment.tax_static_value

        self.amount_change = self.amount_pay - (order_total_amount + amount_deli + type_payment_amount)
        self.amount_final = order_total_amount + amount_deli + type_payment_amount

        Order.objects.filter(uuid=self.order.uuid).update(is_paid=True, is_active=False)

        get_order_items = OrderItem.objects.filter(order=self.order.id)

        for item in get_order_items:
            if (item.product.product.is_stock):
                get_product_inventory = Inventory.objects.filter(product_id=item.product.id).first()
                stock_in_inventory = get_product_inventory.stock
                calculate = stock_in_inventory - item.quantity
                Inventory.objects.filter(product_id=item.product.id).update(stock=calculate)

        if (self.order.is_active):
            get_sales_module = SalesModule.objects.filter(id=self.sales_module.id)
            get_sales_module_first = SalesModule.objects.filter(id=self.sales_module.id).first()
            get_sales_module_old_value = get_sales_module_first.initial_amount
            get_order_old_value = get_sales_module_first.quanity_orders

            calculate = get_sales_module_old_value + self.order.total_amount

            get_sales_module.update(finish_amount=calculate, quanity_orders=get_order_old_value + 1)
            super(Payment, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        Order.objects.filter(id=self.order.id).update(is_active=True, is_paid=False, total_with_taxts=0)
        get_order_items = OrderItem.objects.filter(order=self.order.id)

        for item in get_order_items:
            if (item.product.product.is_stock):
                get_product_inventory = Inventory.objects.filter(product_id=item.product.id).first()
                stock_in_inventory = get_product_inventory.stock
                calculate = stock_in_inventory + item.quantity
                Inventory.objects.filter(product_id=item.product.id).update(stock=calculate)

            sales_module_obj = SalesModule.objects.filter(id=self.sales_module.id).first()
            value_old_amount = sales_module_obj.finish_amount
            value_old_quantity_orders = sales_module_obj.quanity_orders
            SalesModule.objects.filter(id=self.sales_module.id).update(
                finish_amount=value_old_amount - self.order.total_amount, quanity_orders=value_old_quantity_orders - 1)
        super(Payment, self).delete(*args, **kwargs)

    def __str__(self):
        return str(self.order)
