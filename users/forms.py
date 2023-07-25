from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput, EmailInput
from django import forms
from .models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'gender',
                  'password1',
                  'password2'
                  ]
        
        # widgets = {
        #     'first_name': TextInput(attrs={
        #         'class': "form-control",
        #         'style': 'max-width: 300px;',
        #         'placeholder': 'Name'
        #         }),
        #     'last_name': TextInput(attrs={
        #         'class': "form-control",
        #         'style': 'max-width: 300px;',
        #         'placeholder': 'Name'
        #         }),
        #     'email': EmailInput(attrs={
        #         'class': "form-control", 
        #         'style': 'max-width: 300px;',
        #         'placeholder': 'Email'
        #         })
        # }

