from django.shortcuts import render, redirect, get_object_or_404, reverse
from . forms import *
from django.core.mail import send_mail
from django.contrib import messages
import random
from django.conf import settings
from . utils import *
from datetime import datetime
import pyotp
from project import views
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required



def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_team_lead(user):
    return user.groups.filter(name='Team_lead').exists()

def is_team_member(user):
    return user.groups.filter(name='Team_member').exists()


def register(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            # Save the form data in the session temporarily
            request.session['registration_form_data'] = form.cleaned_data
            is_admin = form.cleaned_data.get('is_admin')
            is_team_lead = form.cleaned_data.get('is_team_lead')
            is_team_member = form.cleaned_data.get('is_team_member')

            # Assign user to appropriate groups
            if is_admin:
                group_name = 'Admin'
            elif is_team_lead:
                group_name = 'Team_lead'
            elif is_team_member:
                group_name = 'Team_member'
            else:
                group_name = None  # No group selected

            # If a group is selected, add the user to that group
            request.session['group_name'] = group_name


            # Redirect to OTP input page for verification
            email = form.cleaned_data.get('email')
            send_otp(request, email)
            return redirect('verify_otp')
    else:
        form = UserSignUpForm()
    
    return render(request, 'registration/signup.html', {'form': form})

def verify_otp(request):
    error_message = None
    if request.method == 'POST':
        otp = request.POST.get('otp')
        otp_secret_key = request.session.get('otp_secret_key')

        if otp_secret_key:
            totp = pyotp.TOTP(otp_secret_key, interval=300)
            if totp.verify(otp):
                form_data = request.session.get('registration_form_data')
                group_name = request.session.get('group_name')
                if form_data and group_name:
                    form_data['is_admin'] = group_name == 'Admin'
                    form_data['is_team_lead'] = group_name == 'Team_lead'
                    form_data['is_team_member'] = group_name == 'Team_member'
                    form = UserSignUpForm(form_data)
                    if form.is_valid():
                        user = form.save()
                        if group_name:
                            group = Group.objects.get(name=group_name)
                            user.groups.add(group)
                        username = form.cleaned_data.get('username')
                        messages.success(request, f'Your account has been created! {username}')
                        # Clear session data
                        del request.session['registration_form_data']
                        del request.session['otp_secret_key']
                        del request.session['otp_valid_until']
                        return redirect('login')
                else:
                    error_message = "Invalid OTP"
            else:
                error_message = "OTP has expired"
        else:
            error_message = "OTP verification failed"

    return render(request, 'registration/verify_otp.html', {'error_message': error_message})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    user_roles = {
        'is_admin': is_admin(request.user),
        'is_team_lead': is_team_lead(request.user),
        'is_team_member': is_team_member(request.user),
    }

    return render(request, 'registration/profile.html', {'u_form': u_form, 'user_roles': user_roles, 'p_form': p_form})