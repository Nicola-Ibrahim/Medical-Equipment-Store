from django.db import models
from .utils import slugify_instance_name
from accounts.models import Warehouse

# Create your models here.
class Product(models.Model):
    # TODO: Make a composite foreign key from (id, name, warehouse)
    
    name = models.CharField(max_length=200)
    price = models.FloatField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, null=True)
    visible = models.BooleanField(default=True)
    warehouse = models.ForeignKey(Warehouse, related_name='products', on_delete=models.CASCADE)


    def __str__(self):
        return self.name

    
    def save(self, *args, **kwargs):
        slugify_instance_name(self)
        return super().save(*args, **kwargs)



    # def is_available(self, consume_quantity:int):
    #     diff = self.quantity - consume_quantity

    #     # Abort process if the available quantity bellow 0 value
    #     if(diff < 0):
    #         raise exceptions.ValidationError(f"You exceed the number of available for the {self.name}:{self.base_quantity} / should be {diff} or les")
    