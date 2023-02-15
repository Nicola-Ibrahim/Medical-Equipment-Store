"""
This file contains:
custom user model
proxy models of multiple users type
other models related to user
"""

from itertools import chain

from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from .models_manager import CustomUserManager, ProxyUserManger


class PrintableModel(models.Model):
    def __repr__(self):
        return str(self.to_dict())

    def to_dict(instance):
        opts = instance._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            data[f.name] = f.value_from_object(instance)
        for f in opts.many_to_many:
            data[f.name] = [i.id for i in f.value_from_object(instance)]
        return data

    class Meta:
        abstract = True


class User(AbstractUser, PrintableModel):
    objects = CustomUserManager()

    class Type(models.TextChoices):
        DOCTOR = "Doctor", "doctor"
        DELIVERY_WORKER = "Delivery worker", "delivery worker"
        WAREHOUSE = "Warehouse", "warehouse"
        ADMIN = "Admin", "admin"
        STATISTICIAN = "Statistician", "statistician"
        BASE_ACCOUNTANT = "Base accountant", "base accountant"
        DELIVERY_WORKER_ACCOUNTANT = (
            "Delivery worker accountant",
            "delivery worker accountant",
        )
        WAREHOUSE_ACCOUNTANT = "Warehouse accountant", "warehouse accountant"

    # Set username to none
    username = None
    first_name = None
    last_name = None

    email = models.EmailField(("email address"), unique=True, validators=[validate_email])
    USERNAME_FIELD = "email"  # Set email field as a username
    REQUIRED_FIELDS = ["password"]  # Remove email from required fields

    phone_number = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    identification = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=50, choices=Type.choices, blank=True, default=Type.ADMIN)
    is_verified = models.BooleanField(default=False)
    manager = models.ForeignKey("Admin", on_delete=models.SET_NULL, null=True, blank=True)
    subscription = models.ForeignKey("Subscription", null=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
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


class Subscription(models.Model):
    type = models.CharField(max_length=50)  # type: ignore # noqa: A003
    value = models.PositiveIntegerField()
    details = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.type
