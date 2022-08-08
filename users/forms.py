from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput, DateTimeInput
from .models import DataInput

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class InputOptionsForm(ModelForm):
    class Meta:
        model = DataInput
        fields = ['start_day', 'finish_day', 'campaign_id', 'buyer_id']

        widgets = {
            'start_day': DateTimeInput(attrs={
                'placeholder': '2022-08-07'
            }),
            'finish_day': DateTimeInput(attrs={
                'placeholder': '2022-08-08'
            }),
            'campaign_id': TextInput(attrs={
                'placeholder': 'Campaign Id'
            }),
            'buyer_id': TextInput(attrs={
                'placeholder': 'Buyer Id'
            })
        }

