"""
Представления для управления заказами.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm


@login_required
def order_create(request):
    """
    Создание заказа из корзины.
    Использует транзакции для атомарности операции.
    """
    cart = Cart(request)
    
    # Проверка, что корзина не пуста
    if len(cart) == 0:
        messages.warning(request, 'Ваша корзина пуста.')
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        
        if form.is_valid():
            # Используем транзакцию для атомарности
            with transaction.atomic():
                # Создаем заказ
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                
                # Создаем элементы заказа из корзины
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )
                    
                    # Уменьшаем количество товара на складе
                    product = item['product']
                    product.stock -= item['quantity']
                    product.save()
                
                # Очищаем корзину
                cart.clear()
                
                messages.success(
                    request,
                    f'Заказ #{order.id} успешно создан! '
                    'Мы свяжемся с вами для подтверждения.'
                )
                return redirect('orders:order_detail', order_id=order.id)
        else:
            # Вывод ошибок валидации
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        # Предзаполняем форму данными из профиля
        initial_data = {}
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone': profile.phone,
                'address': profile.address,
                'city': profile.city,
                'postal_code': profile.postal_code,
            }
        
        form = OrderCreateForm(initial=initial_data)
    
    context = {
        'cart': cart,
        'form': form,
    }
    
    return render(request, 'orders/create.html', context)


@login_required
def order_detail(request, order_id):
    """
    Детальная информация о заказе.
    """
    order = get_object_or_404(
        Order.objects.prefetch_related('items__product'),
        id=order_id,
        user=request.user
    )
    
    context = {
        'order': order,
    }
    
    return render(request, 'orders/detail.html', context)


@login_required
def order_list(request):
    """
    Список заказов пользователя.
    """
    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related('items__product').order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'orders/list.html', context)


@login_required
def order_cancel(request, order_id):
    """
    Отмена заказа пользователем.
    Возможна только для заказов в статусе 'pending'.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status != 'pending':
        messages.error(
            request,
            'Невозможно отменить заказ. '
            'Обратитесь в службу поддержки.'
        )
        return redirect('orders:order_detail', order_id=order.id)
    
    if request.method == 'POST':
        with transaction.atomic():
            # Возвращаем товары на склад
            for item in order.items.all():
                product = item.product
                product.stock += item.quantity
                product.save()
            
            # Меняем статус заказа
            order.status = 'cancelled'
            order.save()
            
            messages.success(request, f'Заказ #{order.id} отменен.')
            return redirect('orders:order_list')
    
    context = {
        'order': order,
    }
    
    return render(request, 'orders/cancel_confirm.html', context)
