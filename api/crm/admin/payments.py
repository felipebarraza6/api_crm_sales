"""Payments admin."""

# Django
from django.contrib import admin

# Models
from api.crm.models import Payment, TypePayment

admin.site.register(Payment)
admin.site.register(TypePayment)

