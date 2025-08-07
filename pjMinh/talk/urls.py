from django.urls import path
from . import views

app_name = 'talk'

urlpatterns = [
    path('', views.home, name='home'),
    path('topics/', views.topic_list, name='topic_list'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('topic/<int:topic_id>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('minigame/<int:game_id>/', views.minigame_play, name='minigame_play'),
    path('minigame/<int:game_id>/data/', views.minigame_data, name='minigame_data'),
    path('search-food-link/', views.search_food_link, name='search_food_link'),
]
