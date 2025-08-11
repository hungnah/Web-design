from django.urls import path
from . import views

urlpatterns = [
    path('phrases/', views.phrase_list, name='phrase_list'),
    path('lessons/', views.lessons, name='lessons'),
    path('theory-sections/', views.all_theory_sections, name='all_theory_sections'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lesson/<int:lesson_id>/theory/<int:section_id>/', views.theory_section_detail, name='theory_section_detail'),
    path('lesson/<int:lesson_id>/quiz/', views.lesson_quiz, name='lesson_quiz'),
    path('create-post/<int:phrase_id>/', views.create_post, name='create_post'),
    path('edit-post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('accept-post/<int:post_id>/', views.accept_post, name='accept_post'),
    path('cancel-accept-post/<int:post_id>/', views.cancel_accept_post, name='cancel_accept_post'),
    
    # Partner request URLs
    path('create-partner-request/', views.create_partner_request, name='create_partner_request'),
    path('my-partner-requests/', views.my_partner_requests, name='my_partner_requests'),
    path('accept-partner-request/<int:request_id>/', views.accept_partner_request, name='accept_partner_request'),
]
