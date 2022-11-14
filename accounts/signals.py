"""
This file script should be imported in the ready()
method in apps.py file
For ensuring to be recognizable by the server
"""


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from .models import Warehouse
from .permissions import PermissionGroupsName


@receiver(post_save, sender=Warehouse)
def assign_group(sender, instance, **kwargs):
    """Assign permission group to the user"""

    # Get the warehouse permission groups
    perm_groups = Group.objects.filter(name__in = [
        PermissionGroupsName.WAREHOUSE_GROUP.value,
        PermissionGroupsName.CAN_CHANGE_ORDER.value
    ]) 

    for perm_group in perm_groups:
        # Assign the new instance to the group
        instance.groups.add(perm_group)

    
    
