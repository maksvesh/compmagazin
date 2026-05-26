"""
Административная панель для управления магазином.
"""
from django.contrib import admin
from .models import Category, Product, ProductImage, Review, Wishlist, ViewHistory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Административная панель для категорий"""
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'


class ProductImageInline(admin.TabularInline):
    """Инлайн для дополнительных изображений товара"""
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Административная панель для товаров"""
    list_display = ['name', 'category', 'price', 'stock', 'available', 'created_at', 'views_count']
    list_filter = ['available', 'created_at', 'updated_at', 'category']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'name', 'slug', 'description', 'image')
        }),
        ('Характеристики', {
            'fields': ('specifications',)
        }),
        ('Цена и наличие', {
            'fields': ('price', 'stock', 'available')
        }),
        ('Статистика', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Административная панель для изображений товаров"""
    list_display = ['product', 'alt_text', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['product__name', 'alt_text']
    date_hierarchy = 'uploaded_at'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Административная панель для отзывов"""
    list_display = ['product', 'user', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['product__name', 'user__username', 'comment']
    list_editable = ['is_approved']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Информация об отзыве', {
            'fields': ('product', 'user', 'rating', 'comment')
        }),
        ('Модерация', {
            'fields': ('is_approved',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    """Административная панель для списков желаний"""
    list_display = ['user', 'product', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'product__name']
    date_hierarchy = 'added_at'


@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    """Административная панель для истории просмотров"""
    list_display = ['user', 'product', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['user__username', 'product__name']
    date_hierarchy = 'viewed_at'
    readonly_fields = ['viewed_at']
