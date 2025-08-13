# session/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('study/<int:partner_id>/<int:post_id>/<int:phrase_id>', views.study, name='study'),
    path('evaluate/<int:partner_id>/<int:post_id>/<int:phrase_id>', views.evaluate, name='evaluate'),
    path('submit_evaluation/', views.submit_evaluation, name='submit_evaluation'),
    path('list/', views.list, name='session_list'),
    path('study_phrase/<int:phrase_id>/', views.study_detail, name='study_phrase'),
]
