"""
URL configuration for vietnam_japan_connect project.

This is the main URL router for the Vietnam-Japan language exchange platform.
The URLs are organized by functionality:

- /auth/     -> user_profile.urls (authentication, registration, profiles, dashboards)
- /chat/     -> chat_system.urls (chat rooms, messaging)
- /create/   -> event_creation.urls (creating posts, lessons, partner requests)
- /search/   -> event_search.urls (finding and browsing opportunities)
- /admin/    -> Django admin interface
- /         -> Redirects to dashboard

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),
    
    # Home page redirects to user dashboard
    path('', RedirectView.as_view(url='/auth/dashboard/', permanent=False), name='home'),
    
    # Main application modules
    path('auth/', include('user_profile.urls')),     # User management & authentication
    path('chat/', include('chat_system.urls')),      # Real-time messaging system
    path('create/', include('event_creation.urls')), # Creating posts, lessons, requests
    path('search/', include('event_search.urls')),   # Finding & browsing opportunities
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
