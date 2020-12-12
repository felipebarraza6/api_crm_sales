"""Admin Clients."""

# Django
from django.contrib import admin

# Models
from api.crm.models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display=('id',)
    
admin.site.register(Client, ClientAdmin)
