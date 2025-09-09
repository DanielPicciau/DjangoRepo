from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms 
from django.forms.widgets import PasswordInput, TextInput
from .models import Client

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


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ("name", "company", "email", "phone", "notes")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget = TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Full name'})
        self.fields['company'].widget = TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Company (optional)'})
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Email (optional)'})
        self.fields['phone'].widget = TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Phone (optional)'})
        self.fields['notes'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Notes (optional)'})


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "is_staff")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['first_name'].widget = TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'First name'})
        self.fields['last_name'].widget = TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Last name'})
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Email'})
        # Render is_staff as checkbox with spacing
        self.fields['is_staff'].widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})
