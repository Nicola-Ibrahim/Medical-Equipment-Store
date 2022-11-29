"""
This file script should be imported in the ready()
method in apps.py file
For ensuring to be recognizable by the server
"""


from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

from .models import Order, OrderProduct

@receiver(post_save, sender=OrderProduct)
def decrement_quantity(sender, instance, created, **kwargs):
    """Decrement items quantity after creating an order"""

    if not created:
        return


    """Decrease the base quantity of the product"""
    new_quantity = instance.product.quantity - instance.quantity
    
    # Abort process if the available quantity bellow 0 value
    if(new_quantity < 0):
        raise ValidationError(f"You exceed the number of available for the {instance.product}:{instance.product.quantity}")
        
    instance.product.quantity = new_quantity
    instance.product.save()


@receiver(post_save, sender=OrderProduct)
def add_item_price(sender, instance, created, **kwargs):
    """
    Calculate the total price of an order
    by adding the purchased items on it
    """

    if not created:
        return

    # Get all items of the inserted order
    order = Order.objects.get(id=instance.order.id)

    # Assign total price to the price attribute of the order
    order.price += instance.price
    order.save(update_fields=['price'])    


@receiver(pre_delete, sender=Order)
def increment_quantity(sender, instance, **kwargs):
    """Increment items quantity after deleting an order"""

    # Check if the order is delivered or not
    assert (not instance.status == Order.Status.DELIVERED), ValidationError("The order is delivered and can't be decrement")

    # Get all related items with the order
    order_items = OrderProduct.objects.filter(order=instance)

    # Iterate on each Product to increase the quantity
    for order_item in order_items:
        # product = Product.objects.get(id=order_item.product)
        order_item.product.quantity += order_item.quantity
        order_item.product.save()


