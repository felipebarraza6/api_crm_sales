"""Orders admin."""

# Django
from django.contrib import admin

# Models
from api.crm.models import Delivery

admin.site.register(Delivery)

