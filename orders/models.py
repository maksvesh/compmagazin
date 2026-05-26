"""
Модели для управления заказами.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from shop.models import Product


class Order(models.Model):
    """
    Модель заказа.
    Связывает пользователя с покупкой.
    """
    STATUS_CHOICES = [
        ('pending', 'Ожидает обработки'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )
    
    # Информация о доставке
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.TextField(verbose_name='Адрес доставки')
    city = models.CharField(max_length=100, verbose_name='Город')
    postal_code = models.CharField(max_length=20, verbose_name='Индекс')
    
    # Комментарий к заказу
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    
    # Статус и временные метки
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус',
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    # Оплата
    paid = models.BooleanField(default=False, verbose_name='Оплачен')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f'Заказ #{self.id}'
    
    def get_total_cost(self):
        """Общая стоимость заказа"""
        return sum(item.get_cost() for item in self.items.all())
    
    def get_status_display_class(self):
        """CSS класс для отображения статуса"""
        status_classes = {
            'pending': 'warning',
            'processing': 'info',
            'shipped': 'primary',
            'delivered': 'success',
            'cancelled': 'danger',
        }
        return status_classes.get(self.status, 'secondary')


class OrderItem(models.Model):
    """
    Элемент заказа (товар в заказе).
    Связь ManyToOne с Order и Product.
    """
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Цена'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Количество'
    )
    
    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказов'
    
    def __str__(self):
        return f'{self.quantity}x {self.product.name}'
    
    def get_cost(self):
        """Стоимость элемента заказа"""
        return self.price * self.quantity
