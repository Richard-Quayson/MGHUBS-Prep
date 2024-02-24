from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    
    def create_user(self, firstname, lastname, email, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        
        other_fields.setdefault('is_staff', False)
        other_fields.setdefault('is_superuser', False)
        other_fields.setdefault('is_active', True)

        email = self.normalize_email(email)
        user = self.model(firstname=firstname, lastname=lastname, email=email, password=password, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, firstname, lastname, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assigned to is_staff=True'))
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be assigned to is_superuser=True'))
        
        return self.create_user(firstname, lastname, email, password, **other_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    """
    defines attributes for a custom user model

    Attributes:
        - firstname (CharField): user's first name
        - lastname (CharField): user's last name
        - email (EmailField): user's email address
        - is_staff (BooleanField): user's staff status
        - is_superuser (BooleanField): user's superuser status
        - is_active (BooleanField): user's active status
    """

    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(_('email address'), unique=True)
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstname", "lastname"]

    def __str__(self):
        return f"Name: {self.firstname} {self.lastname}, Email: {self.email}"