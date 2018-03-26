from django import forms
from models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
User = get_user_model()

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = [
            'author',
            'quote_text'
        ]

    # def clean(self, *args, **kwargs):
    #     author = self.cleaned_data.get('author')
    #     quote_text = self.cleaned_data.get('quote_text')
    #
    #     if not author:
    #         raise forms.ValidationError("Quote must have an author")
