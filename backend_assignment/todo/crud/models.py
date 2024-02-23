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
    defines attributes for a User object

    Attributes:
        - firstname (CharField): first name of the user
        - lastname (CharField): last name of the user
        - email (EmailField): email address of the user
        - password (CharField): password of the user
        - is_staff (BooleanField): status of the user
        - is_active (BooleanField): status of the user
        - created_at (DateTimeField): date and time the user was created
        - last_login (DateTimeField): date and time the user last logged in
    """

    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    def __str__(self):
        return f"Name: {self.firstname} {self.lastname}, Email: {self.email}"


class PriorityLevel(models.TextChoices):
    """
    defines the priority levels for a ToDo object
    """

    HIGH = 'High', _('High')
    MEDIUM = 'Medium', _('Medium')
    LOW = 'Low', _('Low')


# class ToDo(models.Model):
    """
    defines attributes for a ToDo object

    Attributes:
        - user (ForeignKey): user who created the ToDo object
        - title (CharField): title of the ToDo object
        - description (TextField): description of the ToDo object
        - priority (CharField): priority level of the ToDo object
        - completed (BooleanField): status of the ToDo object
        - created_at (DateTimeField): date and time the ToDo object was created
        - updated_at (DateTimeField): date and time the ToDo object was last updated
    """

    # priority = models.CharField(max_length=6, choices=PriorityLevel.choices, default=PriorityLevel.LOW)
    # pass