"""salesModule Models."""

# Django
from django.db import models

# Utils
from .utils import ApiModel


class SalesModule(ApiModel):
    user = models.ForeignKey('User', related_name='sales_module_user', null=False, blank=False,
                             on_delete=models.PROTECT)
    initial_amount = models.IntegerField(blank=False, null=False)
    finish_amount = models.IntegerField(blank=False, null=False, default=0)
    quanity_orders = models.IntegerField(blank=False, null=False, default=0)
    date_finish = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str('id: {} - user: {} - created: {}'.format(self.id, self.user, self.created))
