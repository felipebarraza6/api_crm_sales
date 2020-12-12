"""salesModule admin."""

# Django
from django.contrib import admin

# Models
from api.crm.models import SalesModule


admin.site.register(SalesModule)