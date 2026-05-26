"""
Модели для управления пользователями.
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Расширенная информация о пользователе.
    Связь OneToOne с User.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    
    # Контактная информация
    phone = models.CharField(
        max_length=20, 
        blank=True,
        verbose_name='Телефон'
    )
    
    # Адрес доставки
    address = models.TextField(blank=True, verbose_name='Адрес')
    city = models.CharField(max_length=100, blank=True, verbose_name='Город')
    postal_code = models.CharField(max_length=20, blank=True, verbose_name='Индекс')
    
    # Аватар
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    
    # Дополнительная информация
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return f'Профиль {self.user.username}'


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     """Автоматическое создание профиля при регистрации пользователя"""
#     if created:
#         UserProfile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     """Сохранение профиля при сохранении пользователя"""
#     instance.profile.save()
