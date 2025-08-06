from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/setup/', views.profile_setup, name='profile_setup'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/applications/', views.manage_applications, name='manage_applications'),
    path('post/<int:post_id>/chat/', views.chat_room, name='chat_room'),
    path('post/<int:post_id>/send-message/', views.send_message, name='send_message'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('my-applications/', views.my_applications, name='my_applications'),
] 