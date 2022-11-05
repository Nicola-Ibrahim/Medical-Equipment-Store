from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.db.models import Q


# Create your models here.
class UserManager(BaseUserManager):
    """
    Creates and saves a User with the given email and password.
    """
    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email or len(email) <= 0:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create(self, email, password, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    objects = UserManager()

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
    type = models.CharField(max_length=50, choices=Type.choices, blank=True)
    manager = models.ForeignKey("Admin", on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self) -> str:
        return self.first_name


class DoctorManager(UserManager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(type=User.Type.DOCTOR)
    
class Doctor(User):
    class Meta:
        proxy = True

    objects = DoctorManager()

    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.DOCTOR
        return super().save(*args, **kwargs)


class DeliveryWorkerManager(UserManager):
    def get_queryset(self):
        result = super().get_queryset()
        return result.filter(type=User.Type.DELIVERY_WORKER)

class DeliveryWorker(User):

    
    class Meta:
        proxy = True


    objects = DeliveryWorkerManager()

    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.DELIVERY_WORKER
        return super().save(*args, **kwargs)


class WarehouseManager(UserManager):
    def get_queryset(self):
        result = super().get_queryset()
        return result.filter(type=User.Type.WAREHOUSE)

class Warehouse(User):

    
    class Meta:
        proxy = True


    objects = WarehouseManager()

    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.WAREHOUSE
        return super().save(*args, **kwargs)


class WarehouseAccountantManager(UserManager):
    def get_queryset(self):
        result = super().get_queryset()
        return result.filter(type=User.Type.WAREHOUSE_ACCOUNTANT)

class WarehouseAccountant(User):

    class Meta:
        proxy = True


    objects = WarehouseAccountantManager()

    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.WAREHOUSE_ACCOUNTANT
        return super().save(*args, **kwargs)

    

class DeliveryWorkerAccountantManager(UserManager):
    def get_queryset(self):
        result = super().get_queryset()
        return result.filter(type=User.Type.DELIVERY_WORKER_ACCOUNTANT)

class DeliveryWorkerAccountant(User):

    class Meta:
        proxy = True


    objects = DeliveryWorkerAccountantManager()

    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.DELIVERY_WORKER_ACCOUNTANT
        return super().save(*args, **kwargs)

class BaseAccountantManager(UserManager):
    def get_queryset(self):
        result = super().get_queryset()
        return result.filter(type=User.Type.BASE_ACCOUNTANT)

class BaseAccountant(User):

    class Meta:
        proxy = True


    objects = BaseAccountantManager()

    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.BASE_ACCOUNTANT
        return super().save(*args, **kwargs)


class StatisticianManager(UserManager):
    def get_queryset(self):
        result = super().get_queryset()
        return result.filter(type=User.Type.STATISTICIAN)

class Statistician(User):

    class Meta:
        proxy = True


    objects = StatisticianManager()

    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.STATISTICIAN
        return super().save(*args, **kwargs)


class AdminManager(UserManager):
    def get_queryset(self):
        result = super().get_queryset()
        return result.filter(type=User.Type.ADMIN)

class Admin(User):

    class Meta:
        proxy = True


    objects = AdminManager()

    def save(self, *args, **kwargs) -> None:
        self.is_staff = True
        self.is_superuser = True
        self.type = User.Type.ADMIN
        return super().save(*args, **kwargs)