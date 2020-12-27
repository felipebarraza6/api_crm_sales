"""Deliveries Models."""

# Django
from django.db import models

# Utils
from .utils import ApiModel


class Delivery(ApiModel):
    name_service = models.CharField(max_length=120, null=False, blank=False)
    description = models.CharField(max_length=220, null=True, blank=True)
    # porcent
    is_tax_porcent = models.BooleanField(default=False, blank=False, null=False)
    tax_porcent = models.FloatField(null=True, blank=True, default=0.0)
    # static values
    is_tax_static_value = models.BooleanField(default=False, null=False, blank=False)
    tax_static_value = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        verbose_name_plural = 'Deliveries'

    def __str__(self):
        return self.name_service
