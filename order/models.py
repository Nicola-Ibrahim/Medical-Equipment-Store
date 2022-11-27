from django.db import models
from accounts.models import Doctor, DeliveryWorker
from product.models import Product


class Order(models.Model):

    class Status(models.TextChoices):
        # Order status: 1 = Pending; 2 = Processing; 3 = Rejected; 4 = Completed
        PENDING = 'PENDING', 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        SUBMITTED = 'SUBMITTED', 'Submitted'
        DELIVERED = 'DELIVERED', 'Delivered'
        REJECTED = 'REJECTED', 'Rejected'
        COMPLETED = 'COMPLETED', 'Completed'

    status = models.CharField(max_length=20, default=Status.PROCESSING, choices=Status.choices)
    price = models.FloatField(default=0)

    doctor = models.ForeignKey(Doctor, related_name="doctor_orders", on_delete=models.CASCADE)
    delivery_worker = models.ForeignKey(DeliveryWorker, related_name="delivery_worker_orders", on_delete=models.SET_NULL, null=True)

    # Dates
    created_at = models.DateTimeField(auto_now=True)
    required_at = models.DateTimeField(auto_now=True)
    shipped_date = models.DateTimeField(auto_now_add=True)

    # Items
    products = models.ManyToManyField(Product, through='OrderProduct')

    def __str__(self) -> str:
        return f"order-{self.id} by -> " + str(self.doctor)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name='order_set', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_set', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(null=True, blank=True)
    

    def _calc_price(self):
        """
        The method calculates the price value for each 
        product multiply with the inserting quantity
        """
        price_value = self.quantity * self.product.price
        if(self.product.discount > 0):
            price_value *=  self.product.discount / 100
        return price_value


    def save(self, *args, **kwargs):
        self.price = self._calc_price()
        return super().save(*args, **kwargs)


    def __str__(self):
        return f"Order-{str(self.order.id)} -> {str(self.product)}"

    