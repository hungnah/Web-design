from django.urls import path
from . import oauth_views

app_name = 'oauth'

urlpatterns = [
    path('google/', oauth_views.google_oauth_login, name='google_login'),
    path('google/callback/', oauth_views.google_oauth_callback, name='google_callback'),
]
