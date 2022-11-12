"""
This file script should be imported in the ready()
method in apps.py file
For ensuring to be recognizable by the server
"""


from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order, OrderProduct

@receiver(post_save, sender=OrderProduct)
def _add_item_price(sender, instance, **kwargs):
    """
    Calculate the total price of an order
    by adding the purchased items on it
    """

    # Get all items of the inserted order
    order = Order.objects.get(id=instance.order.id)

    # Assign total price to the price attribute of the order
    order.price += instance.price
    order.save(update_fields=['price'])
    
