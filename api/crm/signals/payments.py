"""Signals Payments."""

# Django
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Models
from api.crm.models import Payment, Order, OrderItem, Inventory, Shipping, SalesModule


@receiver(post_delete, sender=Payment)
def post_delete_payment(sender, instance, **kwargs):
    ORDER_INSTANCE = instance.order
    PRODUCTS = OrderItem.objects.filter(order=ORDER_INSTANCE)

    SALES_MODULE_INSTANCE = instance.sales_module
    TYPE_PAYMENT_INSTANCE = instance.type_payment

    if TYPE_PAYMENT_INSTANCE.is_cash:
        SalesModule.objects.filter(id=SALES_MODULE_INSTANCE.id).update(
            initial_amount_cash=SALES_MODULE_INSTANCE.initial_amount_cash - instance.amount_final,
            initial_amount=SALES_MODULE_INSTANCE.initial_amount - instance.amount_final,
            quantity_orders=SALES_MODULE_INSTANCE.quantity_orders - 1
        )
    else:
        SalesModule.objects.filter(id=SALES_MODULE_INSTANCE.id).update(
            initial_amount=SALES_MODULE_INSTANCE.initial_amount - instance.amount_final,
            quantity_orders=SALES_MODULE_INSTANCE.quantity_orders - 1
        )

    if ORDER_INSTANCE.is_delivery:
        Shipping.objects.filter(order=ORDER_INSTANCE).delete()

    Order.objects.filter(id=ORDER_INSTANCE.id).update(
        is_active=True,
        is_paid=False
    )

    for element in PRODUCTS:
        product = element.product.product
        quantity = element.quantity
        stock_available = Inventory.objects.filter(product=product).first().stock
        sustraction_stock = stock_available + quantity
        Inventory.objects.filter(product=product).update(stock=sustraction_stock)


@receiver(post_save, sender=Payment)
def post_payment_created(sender, instance, **kwargs):
    ORDER_INSTANCE = instance.order
    SALES_MODULE_INSTANCE = instance.sales_module
    TYPE_PAYMENT_INSTANCE = instance.type_payment

    # Sales Module
    if TYPE_PAYMENT_INSTANCE.is_cash:
        SalesModule.objects.filter(id=SALES_MODULE_INSTANCE.id).update(
            initial_amount_cash=SALES_MODULE_INSTANCE.initial_amount_cash + instance.amount_final,
            initial_amount=SALES_MODULE_INSTANCE.initial_amount + instance.amount_final,
            quantity_orders=SALES_MODULE_INSTANCE.quantity_orders + 1
        )
    else:
        SalesModule.objects.filter(id=SALES_MODULE_INSTANCE.id).update(
            initial_amount=SALES_MODULE_INSTANCE.initial_amount + instance.amount_final,
            quantity_orders=SALES_MODULE_INSTANCE.quantity_orders + 1
        )

    # Order and Shippings
    ORDER = Order.objects.filter(id=ORDER_INSTANCE.id)
    PRODUCTS = OrderItem.objects.filter(order=ORDER_INSTANCE)

    if ORDER_INSTANCE.is_delivery:
        Shipping.objects.create(
            order=ORDER_INSTANCE,
            delivery=ORDER_INSTANCE.delivery,
            address=ORDER_INSTANCE.client.address_exact,
            note=ORDER_INSTANCE.note_delivery,
        )

    ORDER.update(is_active=False, is_paid=True, is_null=False)

    # Inventory
    for element in PRODUCTS:
        product = element.product.product
        quantity = element.quantity
        stock_available = Inventory.objects.filter(product=product).first().stock
        sustraction_stock = stock_available - quantity
        Inventory.objects.filter(product=product).update(stock=sustraction_stock)

    return instance
