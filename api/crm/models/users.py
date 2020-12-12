#Users Models.

#Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Utils
from .utils import ApiModel


class User(ApiModel, AbstractUser):

    email = models.EmailField(
        'email',
        unique=True,
        error_messages={
            'unique': 'User already exists.'
        }
    )    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email

    
    