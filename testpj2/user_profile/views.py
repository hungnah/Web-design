"""
User Profile Views
Handles user authentication, registration, profile management, and dashboard display.
Supports both Vietnamese and Japanese users with different dashboard experiences.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.http import HttpResponse
from .forms import CustomUserCreationForm, ProfileUpdateForm
from event_creation.models import LanguageExchangePost, PartnerRequest

class CustomLoginView(LoginView):
    """
    Custom login view that redirects already authenticated users to dashboard
    and adds cache control headers to prevent back button issues
    """
    template_name = 'user_profile/login.html'
    success_url = reverse_lazy('dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        # If user is already authenticated, redirect to dashboard
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Add cache control headers to prevent caching
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    def get_success_url(self):
        return reverse('dashboard')

def register(request):
    """
    User registration view supporting both Vietnamese and Japanese users
    Validates age requirement (18+) and creates new user account
    """
    # If user is already authenticated, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create new user and automatically log them in
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Vietnam-Japan Connect!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        # Display empty registration form
        form = CustomUserCreationForm()
    
    response = render(request, 'user_profile/register.html', {'form': form})
    # Add cache control headers to prevent caching
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@login_required
def dashboard(request):
    """
    Main dashboard view with different experiences for Vietnamese and Japanese users
    Japanese users: See their posts and learning materials
    Vietnamese users: See available posts and statistics
    """
    user = request.user
    
    # Set language preference based on nationality
    if user.nationality == 'japanese':
        user.preferred_language = 'ja'
        user.save()
        
        # Get user's recent language exchange posts
        recent_posts = user.japanese_posts.all().select_related('phrase', 'cafe_location')[:5]
        
        context = {
            'user': user,
            'recent_posts': recent_posts,
        }
        return render(request, 'user_profile/japanese_dashboard.html', context)
    else:
        # Vietnamese user dashboard
        # For Vietnamese users, get available posts from Japanese users in their city
        available_posts = LanguageExchangePost.objects.filter(
            japanese_user__nationality='japanese'
        ).select_related('japanese_user', 'phrase', 'cafe_location')
        
        # Filter by user's city if specified
        if user.city and user.city != 'any':
            available_posts = available_posts.filter(cafe_location__city=user.city)
        
        # Only show active posts (not accepted ones)
        available_posts = available_posts.filter(status='active')
        
        # Calculate statistics
        accepted_posts_count = user.vietnamese_posts.filter(status='matched').count()
        available_posts_count = available_posts.filter(status='active').count()
        
        context = {
            'user': user,
            'available_posts': available_posts[:6],  # Show first 6 posts
            'accepted_posts_count': accepted_posts_count,
            'available_posts_count': available_posts_count,
        }
        return render(request, 'user_profile/vietnamese_dashboard.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'user_profile/profile.html', {'form': form})

def guide(request):
    """Hướng dẫn sử dụng web bằng tiếng Nhật hoặc tiếng Việt"""
    language = request.GET.get('lang', 'ja')  # Default to Japanese
    if language == 'vi':
        return render(request, 'user_profile/guide_vi.html')
    else:
        return render(request, 'user_profile/guide.html')