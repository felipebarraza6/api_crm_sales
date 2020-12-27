"""Utils Models."""

#Django
from django.db import models


class ApiModel(models.Model):

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date created'
    )
    
    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date modified'
    )

    class Meta:
        abstract = True
        ordering = ['-created', '-modified']