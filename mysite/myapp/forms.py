from django.contrib.auth.forms import UserCreationForm
from django import forms
from datetime import datetime, timedelta, timezone
from .models import Customer, Goods, BuyModel, ReturnModel


class SignUpForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = [
            'username',
            'password1',
            'password2',
        ]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Goods
        fields = [
            'name',
            'description',
            'price',
            'amount',
        ]


class BuyForm(forms.ModelForm):
    class Meta:
        model = BuyModel
        fields = [
            'amount'
        ]


class ReturnForm(forms.ModelForm):
    class Meta:
        model = ReturnModel
        exclude = [
            'user',
            'purchase',
            'interact_date',
        ]
