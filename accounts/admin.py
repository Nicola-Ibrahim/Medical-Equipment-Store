from django.contrib import admin
from .models import (
    User, 
    Warehouse, 
    DeliveryWorker, 
    Doctor, 
    Admin, 
    BaseAccountant, 
    WarehouseAccountant, 
    DeliveryWorkerAccountant
)

from .profiles import WarehouseProfile


from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
# from django.utils.translation import ugettext_lazy as _


# Register your models here.
admin.site.register([
    Warehouse, 
    DeliveryWorker, 
    Doctor, 
    Admin, 
    BaseAccountant, 
    WarehouseAccountant, 
    DeliveryWorkerAccountant,
    
    WarehouseProfile
])


"""Integrate with admin module."""




@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                        'groups', 'user_permissions', 'type')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)