# CUSTOM USER MODEL MUST BE IN PLACE PRIOR TO FIRST MIGRATION
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

# Make sure to add this app to the settings.py file
# add the following three lines to settings.py
# # WHAT I'M CUSTOMIZING
# # USER SUBSTITUTION
# AUTH_USER_MODEL = 'login_registration.User'

from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


# NOW must edit the AUTH_USER_MODEL
# Create your models here.

# NOW create a Custom manager

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field.
        This User model uses the email field for validation  """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
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


# NOW define the customized User model

class User(AbstractUser):
    """User model."""
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __repr__(self):
        return "User: {}: {}".format(self.first_name, self.email)

