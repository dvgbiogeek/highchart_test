from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
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
                'type': 'password',
                'placeholder': 'Enter password',
                'class': 'form-control',
                })
        }
    error_messages = {
        'username': {'required': "Please enter a correct username and password."},
        'password': {'required': "Please enter a correct username and password."},
        }


class CreateNewForm(forms.ModelForm):
    email = forms.EmailField(required=True,
            widget=forms.EmailInput(attrs={'class': 'form-control',
                'placeholder': 'Enter email address'}))
    password1 = forms.CharField(label="Password", max_length=100,
            widget=forms.PasswordInput(attrs={'class': 'form-control',
                'placeholder': 'Enter password'}))
    password2 = forms.CharField(label="Password Confirmation",
            max_length=100,
            widget=forms.PasswordInput(attrs={'class': 'form-control',
                'placeholder': 'Confirm password'}))
    error_messages = {
        'password_mismatch': _('The two password fields did not match.'),
        'duplicate_username': _('A user with this username already exists'),
    }

    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.fields.TextInput(attrs={
                'placeholder': 'Create a username',
                'class': 'form-control',
                }),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
        except:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(CreateNewForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
