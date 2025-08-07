from django.urls import path
from . import views

app_name = 'food_culture'

urlpatterns = [
    path('', views.food_list, name='food_list'),
    path('food/<int:food_id>/', views.food_detail, name='food_detail'),
    path('region/<str:region>/', views.food_by_region, name='food_by_region'),
    path('cultural-tips/', views.cultural_tips, name='cultural_tips'),
    path('allergen-info/', views.allergen_info, name='allergen_info'),
]
