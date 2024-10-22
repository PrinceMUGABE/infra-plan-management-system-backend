from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, phone, role, password=None, **extra_fields):
        if not first_name:
            raise ValueError('The First Name field is required')
        if not last_name:
            raise ValueError('The Last Name field is required')
        if not phone:
            raise ValueError('The Phone field is required')

        user = self.model(first_name=first_name, last_name=last_name, phone=phone, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(first_name, last_name, phone, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('project_owner', 'Project Owner'),
        ('planner', 'Planner'),
        ('engineer', 'Engineer'),
        ('stakeholder', 'Stakeholder'),
        ('rdb_official', 'RDB Official'),
    ]

    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    phone = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(
            regex=r'^(078|079|073|072)\d{7}$',
            message='Phone number must start with 078, 079, 073, or 072 and be 10 digits long'
        )]
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Removed 'phone' from REQUIRED_FIELDS

    objects = UserManager()

    def __str__(self):
        return self.phone
