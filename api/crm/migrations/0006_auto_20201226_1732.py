# Generated by Django 3.1.4 on 2020-12-26 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_remove_shipping_is_cancelled'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salesmodule',
            old_name='quanity_orders',
            new_name='quantity_orders',
        ),
    ]
