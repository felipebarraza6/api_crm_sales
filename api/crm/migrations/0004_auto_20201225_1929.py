# Generated by Django 3.1.4 on 2020-12-25 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20201225_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipping',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order_shipping', to='crm.order'),
        ),
    ]
