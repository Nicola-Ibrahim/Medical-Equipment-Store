from django.db import models
from django.core import exceptions
from .utils import slugify_instance_name
from accounts.models import Warehouse

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, null=True)
    warehouse = models.ForeignKey(Warehouse, related_name='products', on_delete=models.CASCADE)


    def __str__(self):
        return self.name

    
    def save(self, *args, **kwargs) -> None:
        slugify_instance_name(self)
        return super().save(*args, **kwargs)


    # def is_available(self, consume_quantity:int):
    #     diff = self.quantity - consume_quantity

    #     # Abort process if the available quantity bellow 0 value
    #     if(diff < 0):
    #         raise exceptions.ValidationError(f"You exceed the number of available for the {self.name}:{self.base_quantity} / should be {diff} or les")
    