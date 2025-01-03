"""
Databases Models.
"""
from django.conf import settings # noqa
from django.db import models # noqa
from django.utils.timezone import now # noqa
""" https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser.get_username:~:text=Importing-,AbstractBaseUser,-AbstractBaseUser%20and%20BaseUserManager """ # noqa
from django.contrib.auth.models import ( AbstractBaseUser, BaseUserManager, PermissionsMixin ) # noqa


class UserManager(BaseUserManager):
    """ Manager for user."""

    def create_user(self, email, password=None, **extra_fields):
        """ Creatre, save and return a new user """
        if not email:
            raise ValueError('Users must have an email address.')
        """Pass normalised email to the email field. be4 saving the user"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        """ This set_password will encrypt the password. """
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ Create and save a new superuser """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


""" PermissionsMixin = Functioonality for the permiussions & fields. """


class User(AbstractBaseUser, PermissionsMixin):
    """ User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    """ is_staff, Login with django admin """
    is_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role_id = models.SmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        """Custom save method to update 'updated_at' automatically."""
        self.updated_at = now()
        super().save(*args, **kwargs)

