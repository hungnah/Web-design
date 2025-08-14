"""
Session Security Middleware
Handles session management and prevents back button issues after login
"""

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class SessionSecurityMiddleware:
    """
    Middleware to handle session security
    and handle session management
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if user is authenticated and needs to complete profile
        if request.user.is_authenticated:
            # Skip check for admin users
            if request.user.is_staff:
                return self.get_response(request)
            
            # Check if user needs to complete profile
            if not request.user.gender or not request.user.date_of_birth or not request.user.city:
                # Allow access to profile page and logout
                allowed_paths = [
                    '/auth/profile/',
                    '/auth/logout/',
                    '/admin/',
                ]
                
                current_path = request.path
                if not any(current_path.startswith(path) for path in allowed_paths):
                    # Redirect to profile
                    messages.warning(request, 'Vui lòng hoàn thiện thông tin cá nhân để tiếp tục sử dụng hệ thống.')
                    return redirect('profile')
        
        response = self.get_response(request)
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
