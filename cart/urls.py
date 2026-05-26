"""
URL конфигурация для приложения корзины.
API эндпоинты для работы с корзиной.
"""
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Просмотр корзины
    path('', views.cart_detail, name='cart_detail'),
    
    # API эндпоинты для управления корзиной
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('clear/', views.cart_clear, name='cart_clear'),
]
