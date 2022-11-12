from django.db import models
from accounts.models import Doctor, DeliveryWorker
from warehouse.models import Product


# Create your models here.

class Order(models.Model):
    class Status(models.TextChoices):
        # Order status: 1 = Pending; 2 = Processing; 3 = Rejected; 4 = Completed
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        REJECTED = 'REJECTED', 'Rejected'
        COMPLETED = 'COMPLETED', 'Completed'

    status = models.CharField(max_length=20, default=Status.PROCESSING, choices=Status.choices)
    price = models.FloatField(null=True, blank=True)

    doctor = models.ForeignKey(Doctor, related_name="doctor_orders", on_delete=models.CASCADE)
    delivery_worker = models.ForeignKey(DeliveryWorker, related_name="delivery_worker_orders", on_delete=models.SET_NULL, null=True)

    # Flags
    accepted = models.BooleanField(default=False)
    submitted = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    # Dates
    created_at = models.DateTimeField(auto_now=True)
    required_at = models.DateTimeField(auto_now=True)
    shipped_date = models.DateTimeField(auto_now_add=True)

    # Items
    items = models.ManyToManyField(Product, through='OrderProduct', related_name='orders')

    def __str__(self) -> str:
        return f"order-{self.id} by -> " + str(self.doctor)

    # def _calc_total_price(self):
    #     order_items = OrderProduct.objects.filter(order=self)
    #     total = sum([each_item.price * each_item.consume_quantity for each_item in order_items])
    #     return total

    
    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)


    # def is_available(self, consume_quantity:int):
    #     diff = self.quantity - consume_quantity

    #     # Abort process if the available quantity bellow 0 value
    #     if(diff < 0):
    #         raise exceptions.ValidationError(f"You exceed the number of available for the {self.name}:{self.base_quantity} / should be {diff} or les")


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    discount = models.FloatField(default=0)
    price = models.FloatField(null=True, blank=True)
    

    def _calc_price(self):
        price_value = self.quantity * self.product.price
        if(self.discount > 0):
            price_value *=  self.discount / 100
        return price_value


    def save(self, *args, **kwargs):
        self.price = self._calc_price()
        return super().save(*args, **kwargs)


    def __str__(self):
        return f"Order-{str(self.order.id)} -> {str(self.product)}"

    