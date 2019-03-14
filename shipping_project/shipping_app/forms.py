
#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from shipping_app import models as shipping_models


# General Forms
class LoginForm(AuthenticationForm):
    """
    """

    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': u'Nombre de Usuario'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': u'Contraseña'}))


# Shipping Forms
class ConfirmationForm(forms.Form):
    """
    """

    ok = forms.IntegerField(widget=forms.HiddenInput(), initial=1, label='')


class CheckoutForm(forms.Form):
    """
    """

    num_products = forms.IntegerField(label='Número de Productos', required=True, widget=forms.TextInput(attrs={'placeholder': u'2'}))
    weight = forms.IntegerField(label='Peso', required=True, widget=forms.TextInput(attrs={'placeholder': u'3.00'}))
    postal_code = forms.CharField(label='Código Postal', required=True, widget=forms.TextInput(attrs={'placeholder': u'25002'}))

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.fields['country'] = forms.ModelChoiceField(
            label='País',
            required=True,
            queryset=shipping_models.Country.objects.all())
        self.fields['region'] = forms.ModelChoiceField(
            label='Comunidad Autónoma',
            required=True,
            queryset=shipping_models.Region.objects.all())
        self.fields['province'] = forms.ModelChoiceField(
            label='Provincia',
            required=True,
            queryset=shipping_models.Province.objects.all())


def get_custom_form(entry_model, entry_fields):
    """
    """

    fields_list = []
    [fields_list.append(field.name) for field in entry_fields]

    class _CustomForm(forms.ModelForm):

        class Meta:
            model = entry_model
            fields = fields_list

    return _CustomForm
