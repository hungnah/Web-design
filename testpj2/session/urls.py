# session/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('study/<int:partner_id>/<int:post_id>/<int:phrase_id>', views.study, name='study'),
    path('study/<int:partner_id>/<int:post_id>/', views.study, name='study_no_phrase'),
    path('evaluate/<int:partner_id>/<int:post_id>/<int:phrase_id>', views.evaluate, name='evaluate'),
    path('evaluate/<int:partner_id>/<int:post_id>/', views.evaluate, name='evaluate_no_phrase'),
    path('submit_evaluation/', views.submit_evaluation, name='submit_evaluation'),
    path('list/', views.list, name='session_list'),
    path('study_phrase/<int:phrase_id>/', views.study_detail, name='study_phrase'),
    path('text-session/<int:post_id>', views.text_session, name='text_session'),
    path('start-chat/<int:post_id>/', views.start_chat_session, name='start_chat_session'),
    path('start-learning/<int:partner_id>/<int:post_id>/<int:phrase_id>/', views.start_learning_session, name='start_learning_session'),
    path('start-working/<int:post_id>/', views.start_working_session, name='start_working_session'),
]
