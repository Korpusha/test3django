from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db.models import Q
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
        fields = ('amount',)


class ReturnForm(forms.ModelForm):
    class Meta:
        model = ReturnModel
        exclude = ('user', 'return_date',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        good_id = kwargs.pop('good_id', None)
        super(ReturnForm, self).__init__(*args, **kwargs)
        self.fields['purchase'] = forms.ModelChoiceField(
            queryset=BuyModel.objects.filter(
                Q(user=user) &
                Q(good__id=good_id) &
                Q(interact_date__gte=(datetime.now(timezone.utc) - timedelta(minutes=3)).astimezone())
            )
        )



