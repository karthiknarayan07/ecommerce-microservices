from django.db import models

from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.core.validators import MinValueValidator ,MaxValueValidator


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, mobile, password=None, **extra_fields):
        if not mobile:
            raise ValueError("The mobile must be set")
        
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role','SUPERADMIN')
        extra_fields.setdefault('custom_permissions',['is_superadmin',])

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(mobile, password, **extra_fields)
    


class UserMaster(AbstractBaseUser):
    
    ROLE_CHOICES = (
        ('SUPERADMIN', 'SUPERADMIN'),
        ('ENDUSER', 'ENDUSER'),
    )
    
    mobile = models.BigIntegerField(unique=True, null=False, blank=False, validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    full_name = models.CharField(max_length=100, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)
    
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='ENDUSER',blank=False,null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    custom_permissions = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50, default='SYSTEM')
    updation_date = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=60,default='SYSTEM')

    objects = CustomUserManager()
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'usermaster'
        indexes = [
            models.Index(fields=['mobile'])
        ]