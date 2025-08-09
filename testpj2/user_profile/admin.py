"""
User Profile Admin Configuration
Provides Django admin interface for managing users:
- Custom user model with Vietnamese and Japanese nationality support
- Extended user fields for language exchange platform
- Age validation and profile management
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for managing platform users
    Extends Django's built-in UserAdmin with additional fields for language exchange
    """
    # Forms used for creating and editing users
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    # Display configuration for user list
    list_display = ('username', 'email', 'full_name', 'nationality', 'city', 'is_staff', 'is_active',)
    list_filter = ('nationality', 'city', 'is_staff', 'is_active',)
    
    # Field organization for editing existing users
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'full_name', 'date_of_birth', 'gender', 'nationality', 'city', 'profile_picture')}),
        ('Additional info', {'fields': ('bio', 'interests', 'preferred_language')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    
    # Field organization for creating new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'full_name', 'date_of_birth', 'gender', 'nationality', 'city', 'is_staff', 'is_active')}
        ),
    )
    
    # Search and ordering configuration
    search_fields = ('username', 'email', 'full_name')
    ordering = ('username',)

# Register the custom user admin
admin.site.register(CustomUser, CustomUserAdmin)