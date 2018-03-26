# CUSTOM USER MODEL MUST BE IN PLACE PRIOR TO FIRST MIGRATION
# DON'T FORGET TO EDIT THE DJANGO ADMIN TO USE THE NEW USER CLASS
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import models
# from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.dispatch import receiver


# should be able to use User and Profile from the user management stuff I already created

class Quote(models.Model):
    author = models.CharField(max_length=255, null=False)
    quote_text = models.TextField(max_length=1000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contributor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='submitted_quotes')
    fave_users = models.ManyToManyField(get_user_model(), related_name='fave_quotes')

    def __repr__(self):
        return "Quote: {}".format(self.quote_text)

