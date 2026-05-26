"""
Представления для управления пользователями.
Включает регистрацию, авторизацию, управление профилем.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import UserProfile
from orders.models import Order


def register(request):
    """
    Регистрация нового пользователя.
    Включает валидацию данных и автоматический вход после регистрации.
    """
    if request.user.is_authenticated:
        messages.info(request, 'Вы уже авторизованы.')
        return redirect('shop:index')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            # Создание пользователя
            user = form.save()
            
            # Автоматический вход
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(
                    request, 
                    f'Добро пожаловать, {username}! Ваш аккаунт успешно создан.'
                )
                return redirect('shop:index')
        else:
            # Вывод ошибок валидации
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    """
    Вход пользователя в систему.
    Поддержка функции "Запомнить меня" через сессии.
    """
    if request.user.is_authenticated:
        messages.info(request, 'Вы уже авторизованы.')
        return redirect('shop:index')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Управление сессиями: "Запомнить меня"
                if not remember_me:
                    # Сессия до закрытия браузера
                    request.session.set_expiry(0)
                else:
                    # Сессия на 2 недели (по умолчанию в settings.py)
                    request.session.set_expiry(1209600)
                
                messages.success(request, f'Добро пожаловать, {username}!')
                
                # Редирект на следующую страницу или на главную
                next_url = request.GET.get('next', 'shop:index')
                return redirect(next_url)
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    """
    Выход пользователя из системы.
    Очистка сессии и cookies.
    """
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('shop:index')


@login_required
def profile(request):
    """
    Просмотр и редактирование профиля пользователя.
    """
    if request.method == 'POST':
        form = UserProfileForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile,
            user=request.user
        )
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('users:profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserProfileForm(
            instance=request.user.profile,
            user=request.user
        )
    
    # История заказов пользователя
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'form': form,
        'orders': orders,
    }
    
    return render(request, 'users/profile.html', context)


@login_required
def order_history(request):
    """
    История заказов пользователя.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'users/order_history.html', context)
