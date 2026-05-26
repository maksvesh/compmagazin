"""
Формы для создания заказов.
"""
from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """
    Форма для создания заказа.
    Включает валидацию всех полей.
    """
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'postal_code', 'comment'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Иван'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Иванов'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@mail.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (___) ___-__-__'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Улица, дом, квартира'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Москва'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '123456'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Дополнительная информация (необязательно)'
            })
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone': 'Телефон',
            'address': 'Адрес доставки',
            'city': 'Город',
            'postal_code': 'Почтовый индекс',
            'comment': 'Комментарий к заказу'
        }
    
    def clean_first_name(self):
        """Валидация имени"""
        first_name = self.cleaned_data.get('first_name', '')
        
        if len(first_name) < 2:
            raise ValidationError('Имя должно содержать не менее 2 символов.')
        
        if not re.match(r'^[а-яА-ЯёЁa-zA-Z\s-]+$', first_name):
            raise ValidationError('Имя может содержать только буквы, пробелы и дефисы.')
        
        return first_name.strip()
    
    def clean_last_name(self):
        """Валидация фамилии"""
        last_name = self.cleaned_data.get('last_name', '')
        
        if len(last_name) < 2:
            raise ValidationError('Фамилия должна содержать не менее 2 символов.')
        
        if not re.match(r'^[а-яА-ЯёЁa-zA-Z\s-]+$', last_name):
            raise ValidationError('Фамилия может содержать только буквы, пробелы и дефисы.')
        
        return last_name.strip()
    
    def clean_phone(self):
        """Валидация номера телефона"""
        phone = self.cleaned_data.get('phone', '')
        
        # Убираем все нецифровые символы
        digits = re.sub(r'\D', '', phone)
        
        # Проверяем длину (10-11 цифр для российских номеров)
        if len(digits) < 10 or len(digits) > 11:
            raise ValidationError('Введите корректный номер телефона (10-11 цифр).')
        
        return phone.strip()
    
    def clean_postal_code(self):
        """Валидация почтового индекса"""
        postal_code = self.cleaned_data.get('postal_code', '')
        
        # Убираем пробелы
        postal_code = postal_code.strip()
        
        # Проверяем, что это 6 цифр (российский формат)
        if not re.match(r'^\d{6}$', postal_code):
            raise ValidationError('Почтовый индекс должен состоять из 6 цифр.')
        
        return postal_code
    
    def clean_address(self):
        """Валидация адреса"""
        address = self.cleaned_data.get('address', '')
        
        if len(address) < 10:
            raise ValidationError('Адрес должен содержать не менее 10 символов.')
        
        return address.strip()
