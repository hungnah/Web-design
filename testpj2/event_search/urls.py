from django.urls import path
from . import views

urlpatterns = [
    path('available-posts/', views.available_posts, name='available_posts'),
    path('all-posts/', views.all_posts, name='all_posts'),
    path('find-partners/', views.find_partners, name='find_partners'),
]
