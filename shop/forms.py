"""
Формы для приложения магазина.
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import Review, ProductImage


class ReviewForm(forms.ModelForm):
    """
    Форма для создания отзыва на товар.
    Валидация: рейтинг от 1 до 5, комментарий не менее 10 символов.
    """
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Поделитесь своим мнением о товаре...'
            })
        }
        labels = {
            'rating': 'Оценка',
            'comment': 'Ваш отзыв'
        }
    
    def clean_comment(self):
        """Валидация комментария"""
        comment = self.cleaned_data.get('comment', '')
        if len(comment) < 10:
            raise ValidationError('Отзыв должен содержать не менее 10 символов.')
        return comment
    
    def clean_rating(self):
        """Валидация рейтинга"""
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise ValidationError('Рейтинг должен быть от 1 до 5.')
        return rating


class ProductFilterForm(forms.Form):
    """
    Форма для фильтрации товаров.
    Используется на странице списка товаров.
    """
    SORT_CHOICES = [
        ('-created_at', 'Сначала новые'),
        ('price', 'Цена: по возрастанию'),
        ('-price', 'Цена: по убыванию'),
        ('name', 'По названию (А-Я)'),
        ('-name', 'По названию (Я-А)'),
        ('-views_count', 'Популярные'),
    ]
    
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск товаров...'
        }),
        label='Поиск'
    )
    
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'От'
        }),
        label='Минимальная цена'
    )
    
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'До'
        }),
        label='Максимальная цена'
    )
    
    sort = forms.ChoiceField(
        required=False,
        choices=SORT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Сортировка'
    )
    
    def clean(self):
        """Валидация формы"""
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')
        
        if min_price and max_price and min_price > max_price:
            raise ValidationError(
                'Минимальная цена не может быть больше максимальной.'
            )
        
        return cleaned_data


class ProductImageForm(forms.ModelForm):
    """
    Форма для загрузки изображений товара.
    Валидация размера и типа файла.
    """
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Описание изображения'
            })
        }
        labels = {
            'image': 'Изображение',
            'alt_text': 'Альтернативный текст'
        }
    
    def clean_image(self):
        """Валидация загружаемого изображения"""
        image = self.cleaned_data.get('image')
        
        if image:
            # Проверка размера файла (максимум 5MB)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Размер файла не должен превышать 5 МБ.')
            
            # Проверка типа файла
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            file_extension = image.name.split('.')[-1].lower()
            
            if file_extension not in valid_extensions:
                raise ValidationError(
                    f'Неподдерживаемый формат файла. '
                    f'Разрешены: {", ".join(valid_extensions)}'
                )
        
        return image
