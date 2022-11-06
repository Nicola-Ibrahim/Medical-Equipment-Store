from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Creates and saves a User with the given email and password.
    """

    def __init__(self, user_type):
        super().__init__()
        self.user_type = user_type

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



class DoctorManager(UserManager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(type=self.user_type)


class DeliveryWorkerManager(UserManager):
    def get_queryset(self):
        result = super().get_queryset()
        return result.filter(type=self.user_type)


class WarehouseManager(UserManager):
    def get_queryset(self):
        result = super().get_queryset()
        return result.filter(type=self.user_type)


class WarehouseAccountantManager(UserManager):
    def get_queryset(self):
        result = super().get_queryset()
        return result.filter(type=self.user_type)


class DeliveryWorkerAccountantManager(UserManager):
    def get_queryset(self):
        result = super().get_queryset()
        return result.filter(type=self.user_type)


class BaseAccountantManager(UserManager):
    def get_queryset(self):
        result = super().get_queryset()
        return result.filter(type=self.user_type)


class StatisticianManager(UserManager):
    def get_queryset(self):
        result = super().get_queryset()
        return result.filter(type=self.user_type)


class AdminManager(UserManager):
    def get_queryset(self):
        result = super().get_queryset()
        return result.filter(type=self.user_type)
