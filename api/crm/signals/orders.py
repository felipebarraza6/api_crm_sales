"""Signals Orders."""

# Django
from django.db.models.signals import post_save
from django.dispatch import receiver

# Models
from api.crm.models import Order, OrderItem


@receiver(post_save, sender=OrderItem)
def update_order_sum_totals(sender, instance, **kwargs):
    # instance
    price = instance.product.price
    quantity = instance.quantity
    order = instance.order
    calculate_product = int(quantity * price)

    ORDER = Order.objects.filter(id=order.id)
    ORDER_OBJ = ORDER.first()

    sum_for_update_total_amount = ORDER_OBJ.total_amount + calculate_product

    operation_calculate = sum_for_update_total_amount

    if ORDER_OBJ.is_delivery:
        service_delivery = ORDER_OBJ.delivery
        if service_delivery.is_tax_porcent:
            tax_import = service_delivery.tax_porcent
            operation_calculate = (sum_for_update_total_amount*tax_import) + sum_for_update_total_amount
        elif service_delivery.is_tax_static_value:
            tax_import = service_delivery.tax_static_value
            operation_calculate = sum_for_update_total_amount + tax_import

    ORDER.update(total_amount=sum_for_update_total_amount, total_with_taxts=operation_calculate)

    return instance
