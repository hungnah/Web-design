# session/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('study/<int:post_id>/<int:phrase_id>', views.study, name='study'),
]
