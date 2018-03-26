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
from forms import *
# from apps.core.models import User

@login_required
def quotes_home(request):
    print "reached quotes home. If they are logged in, show the dashboard"
    print "logged in as {}".format(request.user.first_name)

    button_text = "Add this quote!"
    title = "Contribute a quote"
    all_quotes = Quote.objects.all()
    fave_quotes = Quote.objects.filter(fave_users=request.user)
    bank_quotes = Quote.objects.exclude(fave_users=request.user)

    # print "fave quotes for user: ", fave_quotes
    # print "NOT fave quotes (what's left:", bank_quotes

    # print "all quotes:", all_quotes
    #
    # fave_quotes['fave'] = True
    # bank_quotes['fave'] = False

    quote_form = QuoteForm(request.POST or None)

    # if quote_form.is_valid():
    #     author = quote_form.cleaned_data.get('author')
    #     quote_text = quote_form.cleaned_data.get('quote_text')
    #     user = request.user
    #     new_quote = Quote.objects.create(author=author, quote_text=quote_text, contributor=user)
    #     new_quote.save()
    #
    #     print "added quote to db: {}".format(Quote.objects.last())
    #     return redirect('/')
    context = {
        'greeting_name': request.user.profile.alias,
        'quote_form': quote_form,
        'button_text': button_text,
        'title': title,
        'all_quotes': bank_quotes,
        'fave_quotes': fave_quotes,

    }

    return render(request, 'dashboard.html', context)

@login_required
def add_new_quote(request):
    quote_form = QuoteForm(request.POST)
    if quote_form.is_valid():
        author = quote_form.cleaned_data.get('author')
        quote_text = quote_form.cleaned_data.get('quote_text')
        user = request.user
        new_quote = Quote.objects.create(author=author, quote_text=quote_text, contributor=user)
        new_quote.save()

        print "added quote to db: {}".format(Quote.objects.last())
        return redirect('/')

    print "trying to create a quote"
    return HttpResponse('placeholder to create quote')


# I need to send the current user info when creating a new quote

@login_required
def add_favorite(request, quote_id):
    print "reached ADD FAVE"
    # this is going to TOGGLE favorite
    current_quote = Quote.objects.get(id=quote_id)
    print "quote: ", current_quote.quote_text


    current_quote_fave_users = Quote.objects.get(id=quote_id).fave_users.all()
    print "fave users:", current_quote_fave_users

    # if the quote is already a favorite, then make it UN-favorite
    for user in current_quote_fave_users:
        print "user info:", user.id
        if user.id == request.user.id:
            current_quote.fave_users.remove(request.user)
            current_quote.save()
            return redirect('/quotes')
    # otherwise make it a favorite

    current_quote.fave_users.add(request.user)


    # Quote.objects.filter(fave_users=request.user).
    # print "fave users", current_quote.fave_users
    # if Quote.objects.get(id=quote_id).fave_users(id=request.user):
    # if Quote.objects.get(id=quote_id):
    #     print "YES THIS IS A FAVE"
    # this means the user already favorited, so UN fave


    # get current quote and add it to faves
    new_fave = Quote.objects.get(id=quote_id)

    # print "getting new fave:", new_fave
    # print "adding association to user:", request.user


    # new_fave.fave_users.add(request.user)
    # print "trying to save new fave"

    # new_fave.save()
    return redirect('/')
    # return HttpResponse('new fave saved')



@login_required
def delete_quote(request, quote_id):
    del_quote = Quote.objects.get(id=quote_id)
    if request.user == del_quote.contributor:
        Quote.objects.get(id=quote_id).delete()
        print "quote removed forever"

    return redirect('/')


@login_required
def get_quotes_by_user(request, user_id):
    quote_set = Quote.objects.filter(contributor_id=user_id)
    quote_count = quote_set.count()
    contributor = User.objects.get(id=user_id)

    print "count: ", quote_count
    print "quote set:", quote_set

    context = {
        'contributor_name': contributor.profile.alias,
        'quotes': quote_set,
        'quote_count': quote_count,
    }

    return render(request, 'all_quotes_by_user.html', context)

