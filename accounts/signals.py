"""
This file script should be imported in the ready()
method in apps.py file
For ensuring to be recognizable by the server
"""


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from .models import User, Warehouse
from .permissions import PermissionGroupsName


@receiver(post_save, sender=Warehouse)
def assign_group(sender, instance, **kwargs):
    """Assign permission group to the user"""

    # Get the warehouse permission group 
    perm_group = Group.objects.get(name=PermissionGroupsName.WAREHOUSE_GROUP.value) 

    # Assign the new instance to thr group
    instance.groups.add(perm_group)

    
    
