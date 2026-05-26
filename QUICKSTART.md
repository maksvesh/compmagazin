# Быстрый запуск проекта

## Шаг 1: Подготовка окружения

```bash
cd computer_shop
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

## Шаг 2: Установка зависимостей

```bash
pip install -r requirements.txt
```

## Шаг 3: Инициализация базы данных

```bash
# Создание миграций
python manage.py makemigrations shop users cart orders

# Применение миграций
python manage.py migrate
```

## Шаг 4: Создание администратора

```bash
python manage.py createsuperuser

# Введите:
# Username: admin
# Email: admin@example.com
# Password: admin123 (или свой)
```

## Шаг 5: Создание тестовых данных (опционально)

```python
# Запустите Python shell
python manage.py shell

# Вставьте следующий код:
from shop.models import Category, Product
from decimal import Decimal

# Создание категорий
cat1 = Category.objects.create(name='Процессоры', slug='processors', description='Процессоры Intel и AMD')
cat2 = Category.objects.create(name='Видеокарты', slug='videocards', description='Видеокарты NVIDIA и AMD')
cat3 = Category.objects.create(name='Оперативная память', slug='ram', description='DDR4 и DDR5 память')

# Создание товаров
Product.objects.create(
    category=cat1,
    name='Intel Core i7-12700K',
    slug='intel-i7-12700k',
    description='Процессор Intel Core i7 12-го поколения',
    price=Decimal('35000'),
    stock=15,
    available=True,
    specifications={'cores': 12, 'threads': 20, 'frequency': '3.6 GHz'}
)

Product.objects.create(
    category=cat1,
    name='AMD Ryzen 7 5800X',
    slug='amd-ryzen-7-5800x',
    description='Процессор AMD Ryzen 7',
    price=Decimal('28000'),
    stock=10,
    available=True,
    specifications={'cores': 8, 'threads': 16, 'frequency': '3.8 GHz'}
)

Product.objects.create(
    category=cat2,
    name='NVIDIA RTX 4090',
    slug='nvidia-rtx-4090',
    description='Видеокарта NVIDIA GeForce RTX 4090',
    price=Decimal('150000'),
    stock=5,
    available=True,
    specifications={'memory': '24GB GDDR6X', 'tdp': '450W'}
)

Product.objects.create(
    category=cat3,
    name='Corsair Vengeance 32GB DDR5',
    slug='corsair-ddr5-32gb',
    description='Оперативная память DDR5 32GB',
    price=Decimal('15000'),
    stock=20,
    available=True,
    specifications={'capacity': '32GB', 'frequency': '6000 MHz'}
)

print('Тестовые данные созданы!')
exit()
```

## Шаг 6: Запуск сервера

```bash
python manage.py runserver
```

## Шаг 7: Открыть в браузере

- Главная страница: http://localhost:8000
- Админ-панель: http://localhost:8000/admin
- Каталог: http://localhost:8000/products/

## Быстрое тестирование функционала

### 1. Регистрация пользователя
- Перейдите: http://localhost:8000/users/register/
- Заполните форму
- Войдите в систему

### 2. Добавление товара в корзину
- Откройте любой товар
- Нажмите "Добавить в корзину"
- Перейдите в корзину

### 3. Оформление заказа
- В корзине нажмите "Оформить заказ"
- Заполните данные
- Подтвердите заказ

### 4. Просмотр заказов
- Перейдите в профиль
- Откройте "История заказов"

### 5. Добавление отзыва
- Откройте товар
- Прокрутите вниз
- Оставьте отзыв и рейтинг

## Запуск тестов

```bash
# Юнит-тесты
pytest

# С покрытием
pytest --cov

# Нагрузочное тестирование
locust -f locustfile.py --host=http://localhost:8000
# Откройте http://localhost:8089
```

## Типичные проблемы и решения

### Проблема: "No module named 'PIL'"
```bash
pip install Pillow
```

### Проблема: "django.db.utils.OperationalError: no such table"
```bash
python manage.py migrate
```

### Проблема: "CSRF verification failed"
- Убедитесь, что в формах есть `{% csrf_token %}`
- Проверьте настройки CSRF в settings.py

### Проблема: Медиа файлы не отображаются
- Убедитесь, что `DEBUG = True` в settings.py
- Проверьте настройки MEDIA_URL и MEDIA_ROOT
- В production используйте Nginx для раздачи медиа

## Создание дампа данных

```bash
# Экспорт данных
python manage.py dumpdata shop users > fixtures/data.json

# Импорт данных
python manage.py loaddata fixtures/data.json
```

## Полезные команды

```bash
# Очистка базы данных
python manage.py flush

# Создание нового приложения
python manage.py startapp app_name

# Проверка проекта
python manage.py check

# Показать SQL миграции
python manage.py sqlmigrate shop 0001

# Django shell с автоимпортом моделей
python manage.py shell_plus  # требует django-extensions
```

Готово! Проект запущен и готов к работе. 🎉
