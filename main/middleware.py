# middleware.py

from django.shortcuts import redirect
from django.urls import reverse

class RedirectUnauthorizedToHomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add the URL names of your login-only views here
        login_required_views = [
           
            
            # Add more login-only view URL names if needed
        ]

        if not request.user.is_authenticated and request.path in [reverse(view) for view in login_required_views]:
            # Redirect the user to the home page (change "home" to your actual home URL name)
            return redirect('main:home')

        response = self.get_response(request)
        return response

# Add any other custom middleware classes here if needed
