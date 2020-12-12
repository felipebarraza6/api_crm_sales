"""Payments admin."""

# Django
from django.contrib import admin

# Models
from api.crm.models import Config

admin.site.register(Config)

