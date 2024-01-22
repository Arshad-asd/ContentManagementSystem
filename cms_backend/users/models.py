from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin') 
        return self._create_user(email, password, **extra_fields)


class Role(models.TextChoices):
    USER = 'user', 'User'
    AUTHOR = 'author', 'Author'
    ADMIN = 'admin', 'Admin'


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=50, unique=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.USER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Address(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='address', null=True, blank=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return f"{self.city}, {self.state}, {self.country} - {self.pincode}"
