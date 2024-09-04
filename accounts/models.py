from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.urls import reverse
from datetime import date
from django.utils import timezone
from utils import h_encode, h_decode

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        if not password:
            raise ValueError('Password must be prvided')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


genders = (
    ('female', 'Féminin'),
    ('male', 'Masculin'),
)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=255)
    username = models.CharField(
        max_length=255, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(
        max_length=100, unique=True, blank=True, null=True)
    sex = models.CharField(
        max_length=10, choices=genders, blank=True, null=True)
    image = models.ImageField(
        upload_to='uploads/users/profiles', default='../static/imgs/anon.png', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        # return f'{self.last_name} {self.first_name}'
        return f' {self.email.split("@")[0]}'

    def get_hashid(self):
        return h_encode(self.id)

    def get_short_name(self):
        return f' {self.email.split("@")[0]}'
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'




