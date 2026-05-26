"""
URL конфигурация для приложения заказов.
"""
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Создание заказа
    path('create/', views.order_create, name='order_create'),
    
    # Просмотр заказов
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    
    # Отмена заказа
    path('<int:order_id>/cancel/', views.order_cancel, name='order_cancel'),
]
