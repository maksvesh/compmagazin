"""
URL конфигурация для приложения пользователей.
"""
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Регистрация и авторизация
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Профиль пользователя
    path('profile/', views.profile, name='profile'),
    path('orders/', views.order_history, name='order_history'),
]
