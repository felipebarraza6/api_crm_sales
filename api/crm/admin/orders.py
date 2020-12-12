"""Orders admin."""

# Django
from django.contrib import admin

# Models
from api.crm.models import Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)

