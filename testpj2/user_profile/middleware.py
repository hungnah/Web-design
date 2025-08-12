"""
Custom middleware for user_profile app
Handles session management and prevents back button issues after login
"""

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import get_user

class SessionSecurityMiddleware:
    """
    Middleware to prevent users from accessing certain pages after login
    and handle session security
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Process request
        response = self.get_response(request)
        
        # Add security headers to all responses
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        response['X-Frame-Options'] = 'DENY'
        response['X-Content-Type-Options'] = 'nosniff'
        
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Process view before it's executed
        """
        # Skip middleware for static files and admin
        if request.path.startswith('/static/') or request.path.startswith('/admin/'):
            return None
        
        # Check if user is authenticated
        if request.user.is_authenticated:
            # If user is on home page, redirect to dashboard
            if request.path == '/auth/' or request.path == '/auth':
                return redirect('dashboard')
            
            # If user is on login/register page, redirect to dashboard
            if request.path in ['/auth/login/', '/auth/register/']:
                return redirect('dashboard')
        
        return None
