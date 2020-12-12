"""User admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from api.crm.models import User

class CustomUserAdmin(UserAdmin):
    """User model admin."""

    list_display = ('id','email', 'username', 'first_name')

admin.site.register(User, CustomUserAdmin)



