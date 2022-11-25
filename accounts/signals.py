"""
This file script should be imported in the ready()
method in apps.py file
For ensuring to be recognizable by the server
"""


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from .models import Warehouse, Doctor
from .permissions import PermissionGroupsName


@receiver(post_save, sender=Warehouse)
def assign_group(sender, instance, **kwargs):
    """Assign permission group to the user"""

    try:
        # Get the warehouse permission groups
        perm_group = Group.objects.get(name=PermissionGroupsName.WAREHOUSE_GROUP.value) 

    except Group.DoesNotExist:
        pass

    else:
        # Assign the new instance to the group
        perm_group.user_set.add(instance)
    
@receiver(post_save, sender=Doctor)
def assign_group(sender, instance, **kwargs):
    """Assign permission group to the user"""

    try:
        # Get the warehouse permission groups
        perm_group = Group.objects.get(name=PermissionGroupsName.DOCTOR_GROUP.value) 

    except Group.DoesNotExist:
        pass
    else:
        # Assign the new instance to the group
        perm_group.user_set.add(instance)

    
    
