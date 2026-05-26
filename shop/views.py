"""
Представления для приложения магазина.
Реализованы с использованием CBV (Class-Based Views) и ООП принципов.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.http import JsonResponse
from django.urls import reverse_lazy

from .models import Category, Product, Review, Wishlist, ViewHistory
from .forms import ReviewForm, ProductFilterForm


class ProductListView(ListView):
    """
    Представление списка товаров с фильтрацией и поиском.
    Использует ООП наследование от ListView.
    """
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        """Получение отфильтрованного queryset"""
        queryset = Product.objects.filter(available=True).select_related('category')
        
        # Фильтрация по категории
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Поиск
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Фильтры по цене
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Сортировка
        sort = self.request.GET.get('sort', '-created_at')
        valid_sorts = ['price', '-price', 'name', '-name', '-created_at', 'views_count']
        if sort in valid_sorts:
            queryset = queryset.order_by(sort)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Добавление дополнительного контекста"""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['category'] = get_object_or_404(Category, slug=category_slug)
        
        # Форма фильтрации
        context['filter_form'] = ProductFilterForm(self.request.GET)
        context['search_query'] = self.request.GET.get('q', '')
        
        return context


class ProductDetailView(DetailView):
    """
    Детальное представление товара.
    Показывает информацию о товаре, отзывы и рекомендации.
    """
    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'
    
    def get_object(self, queryset=None):
        """Получение объекта и увеличение счетчика просмотров"""
        product = super().get_object(queryset)
        product.increment_views()
        
        # Сохранение в истории просмотров для авторизованных пользователей
        if self.request.user.is_authenticated:
            ViewHistory.objects.get_or_create(
                user=self.request.user,
                product=product
            )
        
        return product
    
    def get_context_data(self, **kwargs):
        """Добавление отзывов и рекомендаций"""
        context = super().get_context_data(**kwargs)
        
        # Отзывы (только одобренные)
        context['reviews'] = self.object.reviews.filter(
            is_approved=True
        ).select_related('user')[:10]
        
        # Форма для отзыва
        if self.request.user.is_authenticated:
            # Проверка, оставлял ли пользователь уже отзыв
            user_review = Review.objects.filter(
                product=self.object,
                user=self.request.user
            ).first()
            
            if user_review:
                context['user_review'] = user_review
            else:
                context['review_form'] = ReviewForm()
        
        # Похожие товары
        context['related_products'] = Product.objects.filter(
            category=self.object.category,
            available=True
        ).exclude(id=self.object.id)[:4]
        
        # Средний рейтинг
        context['average_rating'] = self.object.average_rating()
        context['review_count'] = self.object.review_count()
        
        # Дополнительные изображения
        context['product_images'] = self.object.images.all()
        
        # Проверка наличия в списке желаний
        if self.request.user.is_authenticated:
            context['in_wishlist'] = Wishlist.objects.filter(
                user=self.request.user,
                product=self.object
            ).exists()
        
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """
    Создание отзыва на товар.
    Использует LoginRequiredMixin для проверки авторизации.
    """
    model = Review
    form_class = ReviewForm
    template_name = 'shop/product/detail.html'
    
    def form_valid(self, form):
        """Обработка валидной формы"""
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        
        # Проверка, не оставлял ли пользователь уже отзыв
        if Review.objects.filter(product=product, user=self.request.user).exists():
            messages.warning(self.request, 'Вы уже оставляли отзыв на этот товар.')
            return redirect('shop:product_detail', pk=product.id, slug=product.slug)
        
        form.instance.product = product
        form.instance.user = self.request.user
        form.instance.is_approved = False  # Требует модерации
        
        messages.success(
            self.request, 
            'Спасибо за отзыв! Он будет опубликован после модерации.'
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        """URL для редиректа после успешного создания"""
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        return reverse_lazy(
            'shop:product_detail', 
            kwargs={'pk': product.id, 'slug': product.slug}
        )


class WishlistView(LoginRequiredMixin, ListView):
    """Список желаний пользователя"""
    model = Wishlist
    template_name = 'shop/wishlist.html'
    context_object_name = 'wishlist_items'
    paginate_by = 12
    
    def get_queryset(self):
        """Получение списка желаний текущего пользователя"""
        return Wishlist.objects.filter(
            user=self.request.user
        ).select_related('product__category')


def add_to_wishlist(request, product_id):
    """
    Добавление товара в список желаний.
    API эндпоинт для AJAX запросов.
    """
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False, 
            'message': 'Необходимо войти в систему'
        }, status=401)
    
    product = get_object_or_404(Product, id=product_id)
    
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if created:
        return JsonResponse({
            'success': True,
            'message': 'Товар добавлен в список желаний',
            'in_wishlist': True
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Товар уже в списке желаний',
            'in_wishlist': True
        })


def remove_from_wishlist(request, product_id):
    """
    Удаление товара из списка желаний.
    API эндпоинт для AJAX запросов.
    """
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'message': 'Необходимо войти в систему'
        }, status=401)
    
    product = get_object_or_404(Product, id=product_id)
    
    deleted_count, _ = Wishlist.objects.filter(
        user=request.user,
        product=product
    ).delete()
    
    if deleted_count > 0:
        return JsonResponse({
            'success': True,
            'message': 'Товар удален из списка желаний',
            'in_wishlist': False
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Товар не найден в списке желаний',
            'in_wishlist': False
        })


class ViewHistoryView(LoginRequiredMixin, ListView):
    """История просмотров пользователя"""
    model = ViewHistory
    template_name = 'shop/view_history.html'
    context_object_name = 'history_items'
    paginate_by = 20
    
    def get_queryset(self):
        """Получение истории просмотров с уникальными товарами"""
        return ViewHistory.objects.filter(
            user=self.request.user
        ).select_related('product__category').order_by(
            'product', '-viewed_at'
        ).distinct('product')


def search_autocomplete(request):
    """
    Автодополнение для поиска товаров.
    API эндпоинт для AJAX запросов.
    """
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query),
        available=True
    )[:10]
    
    results = [{
        'id': product.id,
        'name': product.name,
        'price': str(product.price),
        'url': product.get_absolute_url(),
        'image': product.image.url if product.image else None
    } for product in products]
    
    return JsonResponse({'results': results})


def index(request):
    """Главная страница магазина"""
    # Популярные товары (по просмотрам)
    popular_products = Product.objects.filter(
        available=True
    ).order_by('-views_count')[:8]
    
    # Новинки
    new_products = Product.objects.filter(
        available=True
    ).order_by('-created_at')[:8]
    
    # Категории
    categories = Category.objects.all()
    
    context = {
        'popular_products': popular_products,
        'new_products': new_products,
        'categories': categories,
    }
    
    return render(request, 'shop/index.html', context)
