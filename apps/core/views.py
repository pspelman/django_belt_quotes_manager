# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages


from django.contrib.auth import (
    authenticate,
    get_user_model,
    logout,
    login,

)
# Create your views here.

def index(request):

    print "reached index in core"

    print "trying to do users with get_user_model:"
    print ":", get_user_model().objects.all()
    return HttpResponse("working on it...from core")
