# Signals Clients

from django.db.models.signals import post_save
from django.dispatch import receiver

# Models
from api.crm.models import Inventory, Product


@receiver(post_save, sender=Product)
def create_stock_register(sender, instance, created, **kwargs):

    stock = instance.is_stock

    if stock:
        get_inventory = Inventory.objects.filter(product=instance).first()
        if get_inventory is None:
            Inventory.objects.create(product=instance, stock=0, alert_stock=0)
    elif not stock:
        Inventory.objects.filter(product=instance).delete()


