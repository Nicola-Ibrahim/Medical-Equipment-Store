from django.core.validators import MinValueValidator
from django.db import models

from src.apps.accounts.models import Warehouse
from src.apps.accounts.utils import slugify_instance_name


def upload_to(instance, filename):
    print(instance, filename)

    filename, extension = filename.split(".")

    return f"products/{instance.id}/{filename}-{instance.id}.{extension}"


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(validators=[MinValueValidator(1)])
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    discount = models.FloatField(default=0, validators=[MinValueValidator(0)])
    image = models.ImageField(
        upload_to=upload_to, height_field=None, width_field=None, max_length=None, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, null=True)
    visible = models.BooleanField(default=True)
    warehouse = models.ForeignKey(Warehouse, related_name="products", on_delete=models.CASCADE)

    class Meta:
        # Prevent repeated product by forcing the unique const
        unique_together = (
            "name",
            "warehouse",
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slugify_instance_name(self)
        return super().save(*args, **kwargs)

    def is_available(self, consume_quantity: int):
        """Check availability of a product"""

        available_quantity = self.quantity - consume_quantity

        # Abort process if the available quantity bellow 0 value
        if available_quantity < 0:
            return False, available_quantity
        return True, available_quantity
