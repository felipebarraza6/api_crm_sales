"""Products Models."""
#Python
import uuid

#Django
from django.db import models
from django.utils.text import slugify

#Utils
from .utils import ApiModel

#Models
from .deliveries import Delivery

class Category(ApiModel):
    name = models.CharField(max_length=60, blank=False, null=False)
    description = models.TextField(max_length=220, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Product_categories'


class Product(ApiModel):
    #Category product
    category = models.ForeignKey('Category', related_name='product_category', on_delete=models.PROTECT)
    #General Data
    name = models.CharField(max_length=140, blank=False, null=False)
    slug = models.SlugField(max_length=140, blank=True)
    description = models.TextField(max_length=220, blank=True, null=True)

    is_stock = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)        
        super(Product, self).save(*args, **kwargs)        

    def __str__(self):
        return self.name


class Price(ApiModel):
    #Product
    product = models.ForeignKey('Product', blank=False, null=False, on_delete=models.CASCADE)
    #Local Fields
    price = models.IntegerField(blank=False, null=False)
    title = models.CharField(max_length=130,blank=False, null=False)
    #Delivery Option
    is_normal_price = is_delivery = models.BooleanField(default=True)
    is_delivery = models.BooleanField(default=False)
    delivery = models.ForeignKey('Delivery', blank=True, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return str(('{} - {}').format(self.product, self.title))

    class Meta:
        verbose_name_plural = 'Product_prices'

class Inventory(ApiModel):
    #Product
    product = models.OneToOneField('Product', blank=False, null=False, on_delete=models.CASCADE)
    stock = models.IntegerField(blank=False, null=False)
    alert_stock = models.IntegerField(blank=False, null=False)
    #Reference Code
    uuid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)


    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name_plural = 'Product_inventories'




