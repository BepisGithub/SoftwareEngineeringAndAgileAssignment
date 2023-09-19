from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        # Defines the fields in the registration form
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']