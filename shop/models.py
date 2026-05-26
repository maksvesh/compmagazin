"""
Модели для приложения магазина компьютеров.
"""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class Category(models.Model):
    """
    Модель категории товаров.
    Используется для организации товаров по типам (процессоры, видеокарты и т.д.)
    """
    name = models.CharField(max_length=200, verbose_name='Название категории', db_index=True)
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    """
    Модель товара (компьютерные комплектующие и устройства).
    """
    category = models.ForeignKey(
        Category, 
        related_name='products', 
        on_delete=models.CASCADE,
        verbose_name='Категория',
        db_index=True
    )
    name = models.CharField(max_length=200, verbose_name='Название', db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(
        upload_to='products/%Y/%m/%d', 
        blank=True, 
        null=True,
        verbose_name='Изображение'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    
    # Технические характеристики
    specifications = models.JSONField(
        default=dict, 
        blank=True,
        verbose_name='Характеристики',
        help_text='JSON с техническими характеристиками'
    )
    
    # Цена и наличие
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Цена'
    )
    available = models.BooleanField(default=True, verbose_name='Доступен', db_index=True)
    stock = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')
    
    # Метаданные
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['available', 'category']),
        ]
        # Уникальность по категории и slug
        unique_together = [['category', 'slug']]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
    
    def average_rating(self):
        """Средний рейтинг товара"""
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0
    
    def review_count(self):
        """Количество отзывов"""
        return self.reviews.count()
    
    def increment_views(self):
        """Увеличить счетчик просмотров"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class ProductImage(models.Model):
    """
    Дополнительные изображения товара.
    Связь OneToMany с Product.
    """
    product = models.ForeignKey(
        Product, 
        related_name='images', 
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    image = models.ImageField(upload_to='products/%Y/%m/%d', verbose_name='Изображение')
    alt_text = models.CharField(max_length=200, blank=True, verbose_name='Альтернативный текст')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    
    class Meta:
        ordering = ['uploaded_at']
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
    
    def __str__(self):
        return f"Изображение для {self.product.name}"


class Review(models.Model):
    """
    Модель отзыва на товар.
    Пользователь может оставить отзыв с оценкой от 1 до 5.
    """
    product = models.ForeignKey(
        Product, 
        related_name='reviews', 
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Рейтинг'
    )
    comment = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    # Для модерации
    is_approved = models.BooleanField(default=False, verbose_name='Одобрен')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        # Один пользователь может оставить только один отзыв на товар
        unique_together = [['product', 'user']]
        indexes = [
            models.Index(fields=['product', '-created_at']),
            models.Index(fields=['is_approved']),
        ]
    
    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.product.name}"


class Wishlist(models.Model):
    """
    Список желаний пользователя.
    Связь ManyToMany между User и Product.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='wishlist',
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    
    class Meta:
        verbose_name = 'Список желаний'
        verbose_name_plural = 'Списки желаний'
        unique_together = [['user', 'product']]
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class ViewHistory(models.Model):
    """
    История просмотров пользователя.
    Для формирования рекомендаций.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='view_history',
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата просмотра')
    
    class Meta:
        verbose_name = 'История просмотров'
        verbose_name_plural = 'История просмотров'
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['user', '-viewed_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} просмотрел {self.product.name}"
