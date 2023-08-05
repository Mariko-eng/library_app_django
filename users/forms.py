from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput, EmailInput
from django import forms
from .models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'gender',
            'school_id',
            'email',
            'password1',
            'password2'
            ]

class NewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'user_type','email',
            'first_name','last_name',
            'phone_number','gender',
            'school_id']

