from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Trang chủ
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),  # Custom logout view
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/change-password/', views.change_password_ajax, name='change_password_ajax'),
    path('guide/', views.guide, name='guide'),
    path('i18n/', include('django.conf.urls.i18n')),

    # Point exchange URLs
    path('point-exchange/', views.point_exchange, name='point_exchange'),
    path('my-vouchers/', views.my_vouchers, name='my_vouchers'),
    path('voucher-history/', views.voucher_history, name='voucher_history'),
    path('use-voucher/<int:voucher_id>/', views.use_voucher, name='use_voucher'),
]
