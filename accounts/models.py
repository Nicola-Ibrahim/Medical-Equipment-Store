"""
This file contains only user models
Also, proxy models added fot more customization on 
users to get subgroup of users 
"""


from rest_framework_simplejwt.tokens import RefreshToken

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from .models_manager import UserManager, ProxyUserManger


class User(AbstractUser):

    objects = UserManager()

    class Type(models.TextChoices):
        DOCTOR = 'Doctor', 'doctor'
        DELIVERY_WORKER = 'Delivery worker', 'delivery worker'
        WAREHOUSE = 'Warehouse' , 'warehouse'
        ADMIN = 'Admin', 'admin'
        STATISTICIAN = 'Statistician', 'statistician'
        BASE_ACCOUNTANT = 'Base accountant', 'base accountant'
        DELIVERY_WORKER_ACCOUNTANT = 'Delivery worker accountant', 'delivery worker accountant'
        WAREHOUSE_ACCOUNTANT = 'Warehouse accountant', 'warehouse accountant'

    

    # Set username to none
    username = None
    first_name = None
    last_name = None


    email = models.EmailField(('email address'), unique=True, validators=[validate_email])
    USERNAME_FIELD = 'email'        # Set email field as a username
    REQUIRED_FIELDS = ['password']  # Remove email from required fields


    phone_number = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    identification = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=50, choices=Type.choices, blank=True, default=Type.ADMIN)
    is_verified = models.BooleanField(default=False)
    manager = models.ForeignKey("Admin", on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self) -> str:
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class Doctor(User):
    class Meta:
        proxy = True

    objects = ProxyUserManger(User.Type.DOCTOR)

    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.DOCTOR
        return super().save(*args, **kwargs)



class DeliveryWorker(User):

    class Meta:
        proxy = True

        
    objects = ProxyUserManger(User.Type.DELIVERY_WORKER)

    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.DELIVERY_WORKER
        return super().save(*args, **kwargs)




class Warehouse(User):

    class Meta:
        proxy = True

    objects = ProxyUserManger(User.Type.WAREHOUSE)


    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.WAREHOUSE
        return super().save(*args, **kwargs)




class WarehouseAccountant(User):

    class Meta:
        proxy = True


    objects = ProxyUserManger(User.Type.WAREHOUSE_ACCOUNTANT)

    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.WAREHOUSE_ACCOUNTANT
        return super().save(*args, **kwargs)

    


class DeliveryWorkerAccountant(User):

    class Meta:
        proxy = True

    objects = ProxyUserManger(User.Type.DELIVERY_WORKER_ACCOUNTANT)


    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.DELIVERY_WORKER_ACCOUNTANT
        return super().save(*args, **kwargs)


class BaseAccountant(User):

    class Meta:
        proxy = True

    objects = ProxyUserManger(User.Type.BASE_ACCOUNTANT)


    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.BASE_ACCOUNTANT
        return super().save(*args, **kwargs)



class Statistician(User):

    class Meta:
        proxy = True

    objects = ProxyUserManger(User.Type.STATISTICIAN)


    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.STATISTICIAN
        return super().save(*args, **kwargs)



class Admin(User):

    class Meta:
        proxy = True

    objects = ProxyUserManger(User.Type.ADMIN)

    def save(self, *args, **kwargs) -> None:
        self.is_staff = True
        self.is_superuser = True
        self.type = User.Type.ADMIN
        return super().save(*args, **kwargs)



