"""
Формы для корзины покупок.
"""
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class CartAddProductForm(forms.Form):
    """
    Форма для добавления товара в корзину.
    Включает валидацию количества.
    """
    quantity = forms.IntegerField(
        min_value=1,
        max_value=100,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '100'
        }),
        label='Количество',
        validators=[
            MinValueValidator(1, message='Количество должно быть не менее 1'),
            MaxValueValidator(100, message='Количество не должно превышать 100')
        ]
    )
    
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput()
    )
