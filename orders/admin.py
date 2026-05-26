"""
Административная панель для управления заказами.
"""
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Инлайн для элементов заказа"""
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Административная панель для заказов"""
    list_display = [
        'id', 'user', 'first_name', 'last_name',
        'email', 'status', 'paid', 'created_at'
    ]
    list_filter = ['status', 'paid', 'created_at', 'updated_at']
    list_editable = ['status', 'paid']
    search_fields = [
        'id', 'user__username', 'first_name',
        'last_name', 'email', 'phone'
    ]
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('user', 'status', 'paid')
        }),
        ('Информация о получателе', {
            'fields': (
                'first_name', 'last_name', 'email', 'phone'
            )
        }),
        ('Адрес доставки', {
            'fields': ('address', 'city', 'postal_code')
        }),
        ('Дополнительно', {
            'fields': ('comment',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Оптимизация запросов"""
        qs = super().get_queryset(request)
        return qs.select_related('user')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Административная панель для элементов заказов"""
    list_display = ['order', 'product', 'price', 'quantity']
    list_filter = ['order__created_at']
    search_fields = ['order__id', 'product__name']
    raw_id_fields = ['order', 'product']
