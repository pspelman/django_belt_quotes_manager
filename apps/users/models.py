# CUSTOM USER MODEL MUST BE IN PLACE PRIOR TO FIRST MIGRATION
# DON'T FORGET TO EDIT THE DJANGO ADMIN TO USE THE NEW USER CLASS
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.dispatch import receiver

""" UNCOMMENT THIS AFTER INITIAL MIGRATION OF CORE APP 
"""

# Import the User model to work with from the core app
# from django.db.models.loading import get_model
# MyModel1 = get_model('app1', 'MyModel1')


from django.conf import settings

# from django.contrib.auth.forms import


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    alias = models.CharField(max_length=30, blank=True, unique=True)
    # bio = models.TextField(max_length=500, blank=True)
    # location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


# Now need signals so the profile is automatically created/updated whenever User instances are
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# This should be hooking the create_user_profile and save_user_profile to the methods to the User model
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


"""
extra notes down here
"""

# This is supposed to EXTEND the regular User model...meaning it will use the Django authentication and
# add some additional properties to the same DB table
#
# class User(AbstractUser):
#     bio = models.TextField(max_length=500, blank=True)
#     location = models.CharField(max_length=30, blank=True)
#     birth_date = models.DateField(null=True, blank=True)


# EXAMPLE IS A COURSE BEING TAUGHT, the tutor will be tied to an individual authorized user account
# Two ways to do this:
# class Course(models.Model):
#     slug = models.SlugField(max_length=100)
#     name = models.CharField(max_length=100)
#     tutor = models.ForeignKey(User, on_delete=models.CASCADE)

# OR TRY IT THIS WAY, where the AUTH_USER_MODEL is being referenced. This will make this class re-usable for
# class Course(models.Model):
#     slug = models.SlugField(max_length=100)
#     name = models.CharField(max_length=100)
#     tutor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
