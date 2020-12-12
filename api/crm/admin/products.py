"""Products admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from api.crm.models import Product, Category, Price, Inventory

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Price)
admin.site.register(Inventory)
