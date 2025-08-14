"""
Custom decorators for user_profile app
Handles profile completion requirements and other access controls
"""

from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps

def profile_complete_required(view_func):
    """
    Decorator to ensure user has complete profile information
    Redirects to profile completion if gender, date_of_birth, nationality, or city is missing
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Skip check for admin users
            if request.user.is_staff:
                return view_func(request, *args, **kwargs)
            
            # Check if user has complete profile
            if not request.user.gender or not request.user.date_of_birth or not request.user.city:
                messages.warning(request, 'Vui lòng hoàn thiện thông tin cá nhân để tiếp tục sử dụng hệ thống.')
                return redirect('profile')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def complete_profile_required(view_func):
    """
    Decorator that combines login_required and profile_complete_required
    Ensures user is both logged in and has complete profile
    """
    @login_required
    @profile_complete_required
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper
