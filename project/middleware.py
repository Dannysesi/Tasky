# middleware.py
from .views import *
from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            # Redirect unauthenticated users to the login page
            return redirect(reverse('login'))
        
        # Add your role-based redirection logic here
        if is_admin(request.user):
            return redirect(reverse('admin_home'))
        elif is_team_lead(request.user):
            return redirect(reverse('team_lead_home'))
        elif is_team_member(request.user):
            return redirect(reverse('team_member_home'))

        # If none of the above conditions are met, proceed with the request
        response = self.get_response(request)
        return response
