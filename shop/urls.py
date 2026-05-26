"""
URL конфигурация для приложения магазина.
Все эндпоинты API и страниц.
"""
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    
    # Список товаров
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('category/<slug:category_slug>/', 
         views.ProductListView.as_view(), 
         name='product_list_by_category'),
    
    # Детальная страница товара
    path('product/<int:pk>/<slug:slug>/', 
         views.ProductDetailView.as_view(), 
         name='product_detail'),
    
    # Отзывы
    path('product/<int:product_id>/review/', 
         views.ReviewCreateView.as_view(), 
         name='add_review'),
    
    # Список желаний (API эндпоинты)
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('wishlist/add/<int:product_id>/', 
         views.add_to_wishlist, 
         name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', 
         views.remove_from_wishlist, 
         name='remove_from_wishlist'),
    
    # История просмотров
    path('history/', views.ViewHistoryView.as_view(), name='view_history'),
    
    # Автодополнение для поиска (API эндпоинт)
    path('api/search-autocomplete/', 
         views.search_autocomplete, 
         name='search_autocomplete'),
]
