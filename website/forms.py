from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms 
from django.forms.widgets import PasswordInput, TextInput

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add bootstrap classes and placeholders for a better UI
        self.fields['username'].widget = TextInput(attrs={
            'class': 'form-control mb-3', 'placeholder': 'Username'
        })
        self.fields['first_name'].widget = TextInput(attrs={
            'class': 'form-control mb-3', 'placeholder': 'First Name'
        })
        self.fields['last_name'].widget = TextInput(attrs={
            'class': 'form-control mb-3', 'placeholder': 'Last Name'
        })
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control mb-3', 'placeholder': 'Email Address'
        })
        self.fields['password1'].widget = PasswordInput(attrs={
            'class': 'form-control mb-3', 'placeholder': 'Password'
        })
        self.fields['password2'].widget = PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Confirm Password'
        })

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))