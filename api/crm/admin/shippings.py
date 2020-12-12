"""Products admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from api.crm.models import Shipping

admin.site.register(Shipping)

