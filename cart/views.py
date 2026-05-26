"""
Представления для управления корзиной покупок.
API эндпоинты для AJAX запросов.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages

from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


def cart_detail(request):
    """
    Отображение содержимого корзины.
    """
    cart = Cart(request)
    
    # Создаем формы для обновления количества каждого товара
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True}
        )
    
    context = {
        'cart': cart,
    }
    
    return render(request, 'cart/detail.html', context)


@require_POST
def cart_add(request, product_id):
    """
    Добавление товара в корзину.
    API эндпоинт для AJAX запросов.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
        
        # Для AJAX запросов
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'Товар "{product.name}" добавлен в корзину',
                'cart_total': str(cart.get_total_price()),
                'cart_count': len(cart)
            })
        
        messages.success(request, f'Товар "{product.name}" добавлен в корзину.')
        return redirect('cart:cart_detail')
    
    # Если форма невалидна
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)
    
    messages.error(request, 'Ошибка при добавлении товара в корзину.')
    return redirect('shop:product_detail', pk=product_id, slug=product.slug)


@require_POST
def cart_remove(request, product_id):
    """
    Удаление товара из корзины.
    API эндпоинт для AJAX запросов.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    cart.remove(product)
    
    # Для AJAX запросов
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'Товар "{product.name}" удален из корзины',
            'cart_total': str(cart.get_total_price()),
            'cart_count': len(cart)
        })
    
    messages.success(request, f'Товар "{product.name}" удален из корзины.')
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    """
    Обновление количества товара в корзине.
    API эндпоинт для AJAX запросов.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity < 1:
            return JsonResponse({
                'success': False,
                'message': 'Количество должно быть больше 0'
            }, status=400)
        
        # Проверка наличия на складе
        if quantity > product.stock:
            return JsonResponse({
                'success': False,
                'message': f'Недостаточно товара на складе. Доступно: {product.stock}'
            }, status=400)
        
        cart.update_quantity(product_id, quantity)
        
        # Для AJAX запросов
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Количество обновлено',
                'cart_total': str(cart.get_total_price()),
                'cart_count': len(cart),
                'item_total': str(product.price * quantity)
            })
        
        messages.success(request, 'Количество товара обновлено.')
        return redirect('cart:cart_detail')
    
    except ValueError:
        return JsonResponse({
            'success': False,
            'message': 'Неверное значение количества'
        }, status=400)


def cart_clear(request):
    """
    Очистка корзины.
    """
    cart = Cart(request)
    cart.clear()
    
    messages.success(request, 'Корзина очищена.')
    return redirect('cart:cart_detail')
