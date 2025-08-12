"""
Custom decorators for user_profile app
Handles session validation and security checks
"""

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from functools import wraps

def session_required(view_func):
    """
    Decorator to ensure user has valid session and prevent back button issues
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this page.')
            return redirect('login')
        
        # Check if session is valid
        if not request.session.session_key:
            messages.error(request, 'Your session has expired. Please log in again.')
            return redirect('login')
        
        # Check if user is trying to access restricted pages
        restricted_paths = ['/auth/', '/auth', '/auth/login/', '/auth/register/']
        if request.path in restricted_paths:
            messages.info(request, 'Redirecting to dashboard...')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

def prevent_back_button(view_func):
    """
    Decorator to add cache control headers and prevent back button issues
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        
        # Add cache control headers
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        response['X-Frame-Options'] = 'DENY'
        response['X-Content-Type-Options'] = 'nosniff'
        
        return response
    
    return _wrapped_view
