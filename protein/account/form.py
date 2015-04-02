from django import forms
from django.contrib.auth.models import User
# from django.contrib.auth.forms import AuthenticationForm


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.fields.TextInput(attrs={
                'placeholder': 'Enter username',
                'class': 'form-control',
                }),
            'password': forms.fields.TextInput(attrs={
                'placeholder': 'Enter username',
                'class': 'form-control',
                })
        }
        error_messages = {
            'invalid_login': "Please enter a correct username and password."
        }
