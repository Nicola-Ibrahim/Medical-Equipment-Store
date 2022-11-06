from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models_manager import *

# Create your models here.

class User(AbstractUser):

    user_type = 'Admin'

    objects = UserManager(user_type)

    class Type(models.TextChoices):
        DOCTOR = 'DOCTOR', 'doctor'
        DELIVERY_WORKER = 'DELIVERY WORKER', 'delivery worker'
        WAREHOUSE = 'WAREHOUSE' , 'warehouse'
        ADMIN = 'ADMIN', 'admin'
        STATISTICIAN = 'STATISTICIAN', 'statistician'
        BASE_ACCOUNTANT = 'BASE ACCOUNTANT', 'base accountant'
        DELIVERY_WORKER_ACCOUNTANT = 'DELIVERY WORKER ACCOUNTANT', 'delivery worker accountant'
        WAREHOUSE_ACCOUNTANT = 'WAREHOUSE ACCOUNTANT', 'warehouse accountant'

    

    # Set username to none
    username = None
    # first_name = None
    # last_name = None


    email = models.EmailField(('email address'), unique=True)
    USERNAME_FIELD = 'email'

    # Remove email from required fields
    REQUIRED_FIELDS = ['password']


    phone_number = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    identification = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=50, choices=Type.choices, blank=True, default=user_type)
    manager = models.ForeignKey("Admin", on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self) -> str:
        return self.email


class Doctor(User):
    class Meta:
        proxy = True

    user_type = User.Type.DOCTOR
    objects = DoctorManager(user_type)

    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.DOCTOR
        return super().save(*args, **kwargs)



class DeliveryWorker(User):

    
    class Meta:
        proxy = True


    user_type = User.Type.DELIVERY_WORKER
    objects = DeliveryWorkerManager(user_type)

    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.DELIVERY_WORKER
        return super().save(*args, **kwargs)



class Warehouse(User):

    
    class Meta:
        proxy = True

    user_type = User.Type.WAREHOUSE
    objects = WarehouseManager(user_type)


    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.WAREHOUSE
        return super().save(*args, **kwargs)



class WarehouseAccountant(User):

    class Meta:
        proxy = True

    user_type = User.Type.WAREHOUSE_ACCOUNTANT
    objects = WarehouseAccountantManager(user_type)

    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.WAREHOUSE_ACCOUNTANT
        return super().save(*args, **kwargs)

    


class DeliveryWorkerAccountant(User):

    class Meta:
        proxy = True

    user_type = User.Type.DELIVERY_WORKER_ACCOUNTANT
    objects = DeliveryWorkerAccountantManager(user_type)


    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.DELIVERY_WORKER_ACCOUNTANT
        return super().save(*args, **kwargs)


class BaseAccountant(User):

    class Meta:
        proxy = True

    user_type = User.Type.BASE_ACCOUNTANT
    objects = BaseAccountantManager(user_type)


    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.BASE_ACCOUNTANT
        return super().save(*args, **kwargs)



class Statistician(User):

    class Meta:
        proxy = True

    user_type = User.Type.STATISTICIAN
    objects = StatisticianManager(user_type)


    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.STATISTICIAN
        return super().save(*args, **kwargs)



class Admin(User):

    class Meta:
        proxy = True

    user_type = User.Type.ADMIN
    objects = AdminManager(user_type)

    def save(self, *args, **kwargs) -> None:
        self.is_staff = True
        self.is_superuser = True
        self.type = User.Type.ADMIN
        return super().save(*args, **kwargs)