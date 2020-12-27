"""salesModule Models."""

# Django
from django.db import models

# Utils
from .utils import ApiModel


class SalesModule(ApiModel):
    user = models.ForeignKey('User', related_name='sales_module_user', null=False, blank=False,
                             on_delete=models.PROTECT)
    initial_amount = models.IntegerField(blank=False, null=False, default=0)
    finish_amount = models.IntegerField(blank=False, null=False, default=0)
    quantity_orders = models.IntegerField(blank=False, null=False, default=0)
    date_finish = models.DateTimeField(blank=True, null=True)

    initial_amount_cash = models.IntegerField(blank=True, null=True, default=0)

    is_active = models.BooleanField(default=True)
    is_sales_box = models.BooleanField(default=False)
    

    def __str__(self):
        return str('id: {} - user: {} - created: {}'.format(self.id, self.user, self.created))
