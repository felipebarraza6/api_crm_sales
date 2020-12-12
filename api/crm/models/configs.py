"""Configs Models."""

#Django
from django.db import models

#Utils
from .utils import ApiModel


class Config(ApiModel):
    name_enterprise = models.CharField(max_length=55, blank=False, null=False)
    logo = models.ImageField()
    description = models.TextField(max_length=250, blank=True, null=True)
    exact_address = models.CharField(max_length=200, blank=False, null=False)
    
    def __str__(self):
        return str(self.name_enterprise)