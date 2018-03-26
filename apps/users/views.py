# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.functions import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import (
    authenticate,
    get_user_model,
    logout,
    login,

)


from django import forms
from forms import UserLoginForm
from forms import *
# from apps.core.models import User

User = get_user_model()
# Create your views here.


# # using the linked User and Profile classes
# def update_profile(request, user_id):
#     user = User.objects.get(pk=user_id)
#     user.profile.bio = 'Lorem ipsum dollar store'
#     # should never need to call the "Profile" save method, the User save() method should trigger that
#     user.save()


# Knowing beforehand you will need to access a related data, you can prefetch it in a single database query:
# users = User.objects.all().select_related('profile')

@login_required
@transaction.atomic
def update_profile(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, _('Your profile was successfully updated!'))
                print("successfully submitted the update form")
                return redirect('/')
                return redirect('settings:profile')
            else:
                messages.error(request, _('Please correct the error below.'))
        else:
            # current_user = User.objects.get(email='phil_spelman@hotmail.com')
            current_user = request.user
            user_form = UserForm(instance=current_user)
            profile_form = ProfileForm(instance=current_user.profile)
            # user_form = UserForm(instance=request.user)
            # profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form' : profile_form,
    })




def index(request):
    print "reached index in core"

    print "trying to do users with get_user_model:"
    print ":", get_user_model().objects.all()
    all_users = get_user_model().objects.all()

    print "all users: ", all_users

    return HttpResponse("working on it...from core")


def user_profile(request):
    current_user = request.user
    print "current user: ", current_user

    # all_users = User.objects.all()
    print "all users", all_users

    # current_user = User.objects.get(email='bill@phil.com')
    print "id:{} | name: {} ".format(current_user.id, current_user.email)
    current_user.bio = 'this is a new bio'
    current_user.save()
    print "current status: ", current_user.bio

    print "try with different user"
    current_user = User.objects.get(email='phil_spelman@hotmail.com')
    print "id:{} | name: {} ".format(current_user.id, current_user.email)
    # current_user.bio = 'this is a new bio'
    # current_user.save()
    # birth_date = datetime.datetime.strptime('07/20/2015', '%m/%d/%Y').date()
    # print birth_date
    # Profile.objects.create(user_id=1, bio='a long life',location='Seattle', birth_date=birth_date)

    print "all profiles: ", Profile.objects.all()
    # date object
    # datetime.datetime.strptime('07/20/2015', '%m/%d/%Y').date()
    # current_user_profile = Profile.objects.get(user_id=2)
    # print "user_profile returned: ", current_user_profile

    response = "this is the user profile for {}".format(current_user)

    return HttpResponse(response)

    # user = get_user_model()

    # new_user = get_user_model().objects.create(email='bobdole@philspelman.com', password='philspelman')
    # user = Profile.objects.all()
    # user1 = Profile.objects.create('user'=get_user_model().objects.create(email='bobdole@philspelman.com', password='philspelman'), )



    # print 'User: ', user

    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # bio = models.TextField(max_length=500, blank=True)
    # location = models.CharField(max_length=30, blank=True)
    # birth_date = models.DateField(null=True, blank=True)


    return HttpResponse("...Working on it...")
    # user = User.objects.get(email='phil_spelman@hotmail.com')
    # user_form = UserForm(instance=request.user)
    # profile_form = ProfileForm(instance=request.user.profile)
    # user_form = UserForm(instance=get_user_model())
    # profile_form = ProfileForm(instance=user.profile)
    # return render(request, 'profiles/profile.html', {
    #     'user_form': user_form,
    #     'profile_form': profile_form,
    # })


def login_view(request):
    print("Arrived at login. User is authenticated: ", request.user.is_authenticated())
    if request.user.is_authenticated:
        print "Logged in as {}".format(request.user.first_name)
        print "already logged in. Sending to dashboard"
        return redirect('/quotes')
        return HttpResponse("{}, you're already logged in.".format(request.user.first_name))

    # birth_date = datetime.datetime.strptime('06/06/2006', '%m/%d/%Y').date()
    # Profile.objects.create(user_id=2, bio='Bills life...a life of Bills', location='Poux Falls', birth_date=birth_date)
    # print "getting birthday..."
    # birth_date = datetime.datetime.strptime('04/04/2000', '%m/%d/%Y').date()
    # print "creating profile for user 3"
    # Profile.objects.create(user_id=3, bio='Someone has a profile and THIS IS IT!', location='Sammamammmammmammaish', birth_date=birth_date)
    #

    # user_form = UserForm(request.POST, instance=request.user)
    # profile_form = UserLoginForm(request.POST or None)
    user_form = UserLoginForm(request.POST or None)
    # form = UserLoginForm(request.POST or None)
    title = "Login"
    button_text = "Login"
    alt_link = "/register"
    alt_message = "register"


    if user_form.is_valid():
        email = user_form.cleaned_data.get('email')
        password = user_form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        print "user:", user
        print "logging in..."
        # Log them in!
        login(request, user)
        print("user is authenticated: ", request.user.is_authenticated())
        return redirect('/quotes')
        # return redirect('/users/update_profile')
    alt_link = "/register"
    alt_message = "register"
    context = {
        'user_form': user_form,
        'title': title,
        'button_text': button_text,
        'alt_message': alt_message,
        'alt_link': alt_link,
    }
    return render(request, 'form.html', context)

# ONE user form (no profile)
def register_view(request):
    # check if user is logged in and send them elsewhere if they are already logged in
    if request.user.is_authenticated:
        print "already logged in. Sending to dashboard"
        return HttpResponse("{}, you're already logged in.".format(request.user.first_name))
    title = "Register"
    button_text = "BUTTON!!!"
    user_form = UserRegisterForm(request.POST or None)


    if user_form.is_valid():
        user = user_form.save(commit=False)
        password = user_form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        # use these lines if not using custom User model
        # new_user = authenticate(email=user.email, password=password)
        # login(request, new_user)
        login(request, user)
        print("is authenticated?: ", request.user.is_authenticated())
    #     return something
    alt_link = "/login"
    alt_message = "login"
    context = {
        'user_form': user_form,
        'button_text': button_text,
        'title': title,
        'alt_message': alt_message,
        'alt_link': alt_link,
    }

    return render(request, 'form.html', context)



# User form AND Profile
# @login_required
@transaction.atomic
def register_profile(request):

    if request.user.is_authenticated:
        print "already logged in. Sending to dashboard"
        return HttpResponse("{}, you're already logged in.".format(request.user.first_name))

    print "Not logged in...moving to get form"

    title = "Register"
    button_text = "Register"
    user_form = UserRegisterForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None)
    alt_link = "/login"
    alt_message = "login"

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': title,
        'button_text': button_text,
        'alt_message': alt_message,
        'alt_link': alt_link,
    }

    if user_form.is_valid() and profile_form.is_valid():
        print "user and profile forms were valid...now trying to save to db"
        user = user_form.save(commit=False)
        password = user_form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        print "user saved: ", user
        print "user form saved without commit...now moving to profile form"

        profile = profile_form.save(commit=False)
        print "profile stuff from form: ", profile

        print "setting profile.user to the new user"
        profile.user = user

        print "user saved to DB, now trying to save profile to DB"
        profile.save()

        print "getting most recent profile: ", Profile.objects.last()

        print "profile successfully saved to DB"

        login(request, user)
        print("is authenticated?: ", request.user.is_authenticated())
        # return HttpResponse("saved to db...check logs now")

        messages.success(request, _('Profile successfully created!'))
            # print("successfully submitted the registration form")
        return redirect('/quotes')
            # return redirect('settings:profile')

    return render(request, 'form.html', context)



@login_required
def logout_view(request):
    name = request.user.first_name
    logout(request)
    return redirect('/login')

    return HttpResponse('Thanks, {}. You\'ve successfully logged out'.format(name))
    return render(request, 'form.html', {})




