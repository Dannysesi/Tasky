from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class UserSignUpForm(UserCreationForm):
    email = forms.EmailField()
    is_admin = forms.BooleanField(label='Is Admin', required=False)
    is_team_lead = forms.BooleanField(label='Is Team Lead', required=False)
    is_team_member = forms.BooleanField(label='Is Team Member', required=False)

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(label='Enter OTP', max_length=6)

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']

