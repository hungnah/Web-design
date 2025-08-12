# session/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('study/<int:partner_id>/<int:post_id>/<int:phrase_id>', views.study, name='study'),
    path('evaluate/<int:partner_id>/<int:post_id>/<int:phrase_id>', views.evaluate, name='evaluate'),
    path('submit_evaluation/', views.submit_evaluation, name='submit_evaluation'),
]
