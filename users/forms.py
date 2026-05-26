"""
Формы для регистрации, авторизации и управления профилем.
Включает валидацию данных и защиту от CSRF.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    """
    Форма регистрации нового пользователя.
    Включает валидацию email, паролей и проверку уникальности.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        }),
        label='Email'
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя'
        }),
        label='Имя'
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Фамилия'
        }),
        label='Фамилия'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }),
        }
        labels = {
            'username': 'Имя пользователя',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Подтверждение пароля'
        })
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
    
    def clean_email(self):
        """Валидация email на уникальность"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email
    
    def clean_username(self):
        """Валидация имени пользователя"""
        username = self.cleaned_data.get('username')
        
        # Проверка длины
        if len(username) < 3:
            raise ValidationError('Имя пользователя должно содержать не менее 3 символов.')
        
        # Проверка на запрещенные символы
        if not username.isalnum() and '_' not in username:
            raise ValidationError(
                'Имя пользователя может содержать только буквы, цифры и символ подчеркивания.'
            )
        
        return username


class UserLoginForm(AuthenticationForm):
    """
    Форма входа в систему.
    Кастомизированная версия стандартной формы Django.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя или Email',
            'autofocus': True
        }),
        label='Имя пользователя или Email'
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        }),
        label='Пароль'
    )
    
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Запомнить меня'
    )


class UserProfileForm(forms.ModelForm):
    """
    Форма редактирования профиля пользователя.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        }),
        label='Email'
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        label='Имя'
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        label='Фамилия'
    )
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'postal_code', 'date_of_birth', 'avatar']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (___) ___-__-__'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'phone': 'Телефон',
            'address': 'Адрес',
            'city': 'Город',
            'postal_code': 'Индекс',
            'date_of_birth': 'Дата рождения',
            'avatar': 'Аватар'
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['email'].initial = self.user.email
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
    
    def save(self, commit=True):
        """Сохранение профиля и данных пользователя"""
        profile = super().save(commit=False)
        
        if self.user:
            self.user.email = self.cleaned_data['email']
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            
            if commit:
                self.user.save()
        
        if commit:
            profile.save()
        
        return profile
    
    def clean_avatar(self):
        """Валидация аватара"""
        avatar = self.cleaned_data.get('avatar')
        
        if avatar:
            # Проверка размера (максимум 2MB)
            if avatar.size > 2 * 1024 * 1024:
                raise ValidationError('Размер файла не должен превышать 2 МБ.')
            
            # Проверка типа файла
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            file_extension = avatar.name.split('.')[-1].lower()
            
            if file_extension not in valid_extensions:
                raise ValidationError(
                    f'Неподдерживаемый формат файла. '
                    f'Разрешены: {", ".join(valid_extensions)}'
                )
        
        return avatar
