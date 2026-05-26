# Руководство по установке и запуску проекта

## ✅ Созданные файлы проекта

### Конфигурационные файлы
- ✅ `manage.py` - Главный файл управления Django
- ✅ `requirements.txt` - Python зависимости
- ✅ `pytest.ini` - Конфигурация pytest
- ✅ `conftest.py` - Фикстуры для тестов
- ✅ `locustfile.py` - Нагрузочное тестирование

### Проект computer_shop_project/
- ✅ `__init__.py`
- ✅ `settings.py` - Настройки проекта
- ✅ `urls.py` - Главный URL роутинг
- ✅ `wsgi.py` - WSGI конфигурация
- ✅ `asgi.py` - ASGI конфигурация

### Приложение shop/
- ✅ `__init__.py`
- ✅ `apps.py`
- ✅ `models.py` - Модели: Product, Category, Review, Wishlist, ViewHistory, ProductImage
- ✅ `views.py` - Представления магазина
- ✅ `forms.py` - Формы: ReviewForm, ProductFilterForm, ProductImageForm
- ✅ `urls.py` - URL маршруты
- ✅ `admin.py` - Административная панель
- ✅ `tests.py` - Юнит-тесты

### Приложение users/
- ✅ `__init__.py`
- ✅ `apps.py`
- ✅ `models.py` - Модель UserProfile
- ✅ `views.py` - Регистрация, вход, профиль
- ✅ `forms.py` - UserRegistrationForm, UserLoginForm, UserProfileForm
- ✅ `urls.py` - URL маршруты
- ✅ `admin.py` - Админ-панель

### Приложение cart/
- ✅ `__init__.py`
- ✅ `apps.py`
- ✅ `cart.py` - Класс Cart (бизнес-логика)
- ✅ `context_processors.py` - Context processor
- ✅ `views.py` - API корзины
- ✅ `forms.py` - CartAddProductForm
- ✅ `urls.py` - URL маршруты

### Приложение orders/
- ✅ `__init__.py`
- ✅ `apps.py`
- ✅ `models.py` - Order, OrderItem
- ✅ `views.py` - Создание и управление заказами
- ✅ `forms.py` - OrderCreateForm
- ✅ `urls.py` - URL маршруты
- ✅ `admin.py` - Админ-панель

### Шаблоны templates/
- ✅ `base.html` - Базовый шаблон
- ✅ `shop/index.html` - Главная страница
- ✅ `shop/product/list.html` - Список товаров
- ✅ `shop/product/detail.html` - Детальная страница товара
- ✅ `shop/wishlist.html` - Список желаний
- ✅ `shop/view_history.html` - История просмотров
- ✅ `users/register.html` - Регистрация
- ✅ `users/login.html` - Вход
- ✅ `users/profile.html` - Профиль пользователя
- ✅ `users/order_history.html` - История заказов
- ✅ `cart/detail.html` - Корзина
- ✅ `orders/create.html` - Оформление заказа
- ✅ `orders/detail.html` - Детали заказа
- ✅ `orders/list.html` - Список заказов
- ✅ `orders/cancel_confirm.html` - Подтверждение отмены

### Документация
- ✅ `README.md` - Основная документация
- ✅ `QUICKSTART.md` - Быстрый старт
- ✅ `PROJECT_STRUCTURE.md` - Структура проекта
- ✅ `INSTALLATION_GUIDE.md` - Этот файл

## 📦 Установка

### Шаг 1: Клонирование/копирование проекта

Скопируйте всю папку `computer_shop` на ваш компьютер.

### Шаг 2: Создание виртуального окружения

```bash
cd computer_shop
python -m venv venv
```

### Шаг 3: Активация виртуального окружения

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Шаг 4: Установка зависимостей

```bash
pip install -r requirements.txt
```

Если возникают проблемы с сетью, установите вручную:

```bash
pip install Django==5.0.1
pip install Pillow==10.2.0
pip install pytest==7.4.4
pip install pytest-django==4.7.0
pip install django-crispy-forms==2.1
pip install crispy-bootstrap4==2.0
pip install locust==2.20.0
```

### Шаг 5: Создание миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

**Ожидаемый вывод:**
```
Migrations for 'shop':
  shop/migrations/0001_initial.py
    - Create model Category
    - Create model Product
    ...
    
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

### Шаг 6: Создание суперпользователя

```bash
python manage.py createsuperuser
```

Введите:
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123` (или свой пароль)

### Шаг 7: Запуск сервера

```bash
python manage.py runserver
```

**Вывод:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Шаг 8: Открыть в браузере

- **Главная страница**: http://127.0.0.1:8000/
- **Админ-панель**: http://127.0.0.1:8000/admin
- **Каталог**: http://127.0.0.1:8000/products/

## 🎯 Создание тестовых данных

### Через Django Shell

```bash
python manage.py shell
```

Вставьте код:

```python
from shop.models import Category, Product
from decimal import Decimal

# Создание категорий
cat1 = Category.objects.create(
    name='Процессоры',
    slug='processors',
    description='Процессоры Intel и AMD для компьютеров'
)

cat2 = Category.objects.create(
    name='Видеокарты',
    slug='videocards',
    description='Графические ускорители NVIDIA и AMD'
)

cat3 = Category.objects.create(
    name='Оперативная память',
    slug='ram',
    description='DDR4 и DDR5 память для компьютеров'
)

cat4 = Category.objects.create(
    name='Материнские платы',
    slug='motherboards',
    description='Материнские платы различных форм-факторов'
)

# Создание товаров - Процессоры
Product.objects.create(
    category=cat1,
    name='Intel Core i7-12700K',
    slug='intel-i7-12700k',
    description='Процессор Intel Core i7 12-го поколения с 12 ядрами и 20 потоками. Отличная производительность для игр и работы.',
    price=Decimal('35000'),
    stock=15,
    available=True,
    specifications={
        'Ядра': '12 (8P+4E)',
        'Потоки': '20',
        'Базовая частота': '3.6 ГГц',
        'Максимальная частота': '5.0 ГГц',
        'Сокет': 'LGA1700',
        'TDP': '125W'
    }
)

Product.objects.create(
    category=cat1,
    name='AMD Ryzen 7 5800X',
    slug='amd-ryzen-7-5800x',
    description='Мощный процессор AMD Ryzen 7 на архитектуре Zen 3. Идеален для игр и многозадачности.',
    price=Decimal('28000'),
    stock=20,
    available=True,
    specifications={
        'Ядра': '8',
        'Потоки': '16',
        'Базовая частота': '3.8 ГГц',
        'Максимальная частота': '4.7 ГГц',
        'Сокет': 'AM4',
        'TDP': '105W'
    }
)

Product.objects.create(
    category=cat1,
    name='Intel Core i5-12400F',
    slug='intel-i5-12400f',
    description='Бюджетный процессор Intel Core i5 без встроенной графики. Отличное соотношение цена/качество.',
    price=Decimal('15000'),
    stock=30,
    available=True,
    specifications={
        'Ядра': '6',
        'Потоки': '12',
        'Базовая частота': '2.5 ГГц',
        'Максимальная частота': '4.4 ГГц',
        'Сокет': 'LGA1700',
        'TDP': '65W'
    }
)

# Видеокарты
Product.objects.create(
    category=cat2,
    name='NVIDIA GeForce RTX 4090',
    slug='nvidia-rtx-4090',
    description='Топовая видеокарта NVIDIA на архитектуре Ada Lovelace. Максимальная производительность в играх и работе.',
    price=Decimal('150000'),
    stock=5,
    available=True,
    specifications={
        'Чип': 'AD102',
        'Память': '24 ГБ GDDR6X',
        'Частота GPU': '2520 МГц',
        'Шина памяти': '384 бит',
        'TDP': '450W',
        'Разъемы': '3x DisplayPort, 1x HDMI'
    }
)

Product.objects.create(
    category=cat2,
    name='AMD Radeon RX 7900 XTX',
    slug='amd-rx-7900-xtx',
    description='Флагманская видеокарта AMD на архитектуре RDNA 3. Отличная производительность и поддержка трассировки лучей.',
    price=Decimal('95000'),
    stock=8,
    available=True,
    specifications={
        'Чип': 'Navi 31',
        'Память': '24 ГБ GDDR6',
        'Частота GPU': '2500 МГц',
        'Шина памяти': '384 бит',
        'TDP': '355W',
        'Разъемы': '2x DisplayPort, 1x HDMI, 1x USB-C'
    }
)

Product.objects.create(
    category=cat2,
    name='NVIDIA GeForce RTX 4060 Ti',
    slug='nvidia-rtx-4060-ti',
    description='Видеокарта среднего класса с отличной производительностью в Full HD и 1440p.',
    price=Decimal('45000'),
    stock=12,
    available=True,
    specifications={
        'Чип': 'AD106',
        'Память': '8 ГБ GDDR6',
        'Частота GPU': '2535 МГц',
        'Шина памяти': '128 бит',
        'TDP': '160W',
        'Разъемы': '3x DisplayPort, 1x HDMI'
    }
)

# Оперативная память
Product.objects.create(
    category=cat3,
    name='Corsair Vengeance DDR5 32GB (2x16GB)',
    slug='corsair-ddr5-32gb',
    description='Высокоскоростная память DDR5 для современных платформ Intel и AMD.',
    price=Decimal('15000'),
    stock=25,
    available=True,
    specifications={
        'Объем': '32 ГБ (2x16 ГБ)',
        'Тип': 'DDR5',
        'Частота': '6000 МГц',
        'Тайминги': 'CL36',
        'Напряжение': '1.35V',
        'Радиаторы': 'Да'
    }
)

Product.objects.create(
    category=cat3,
    name='G.Skill Trident Z5 RGB 64GB (2x32GB)',
    slug='gskill-ddr5-64gb',
    description='Премиальная память DDR5 с RGB подсветкой и высокой частотой.',
    price=Decimal('28000'),
    stock=10,
    available=True,
    specifications={
        'Объем': '64 ГБ (2x32 ГБ)',
        'Тип': 'DDR5',
        'Частота': '6400 МГц',
        'Тайминги': 'CL32',
        'RGB': 'Да',
        'Радиаторы': 'Да'
    }
)

Product.objects.create(
    category=cat3,
    name='Kingston Fury Beast DDR4 16GB (2x8GB)',
    slug='kingston-ddr4-16gb',
    description='Надежная память DDR4 для платформ предыдущего поколения.',
    price=Decimal('5500'),
    stock=40,
    available=True,
    specifications={
        'Объем': '16 ГБ (2x8 ГБ)',
        'Тип': 'DDR4',
        'Частота': '3200 МГц',
        'Тайминги': 'CL16',
        'Напряжение': '1.35V',
        'Радиаторы': 'Да'
    }
)

# Материнские платы
Product.objects.create(
    category=cat4,
    name='ASUS ROG MAXIMUS Z790 HERO',
    slug='asus-z790-hero',
    description='Топовая материнская плата для процессоров Intel 12-13 поколения с расширенными возможностями разгона.',
    price=Decimal('55000'),
    stock=7,
    available=True,
    specifications={
        'Чипсет': 'Intel Z790',
        'Сокет': 'LGA1700',
        'Форм-фактор': 'ATX',
        'Память': 'DDR5, 4 слота, до 128 ГБ',
        'Слоты PCIe': '3x PCIe 4.0 x16',
        'Сеть': '2.5 Гбит/с LAN, Wi-Fi 6E'
    }
)

Product.objects.create(
    category=cat4,
    name='MSI MAG B650 TOMAHAWK WIFI',
    slug='msi-b650-tomahawk',
    description='Материнская плата среднего класса для процессоров AMD Ryzen 7000 серии.',
    price=Decimal('25000'),
    stock=15,
    available=True,
    specifications={
        'Чипсет': 'AMD B650',
        'Сокет': 'AM5',
        'Форм-фактор': 'ATX',
        'Память': 'DDR5, 4 слота, до 128 ГБ',
        'Слоты PCIe': '2x PCIe 4.0 x16',
        'Сеть': '2.5 Гбит/с LAN, Wi-Fi 6E'
    }
)

print('✅ Тестовые данные созданы!')
print(f'Категорий: {Category.objects.count()}')
print(f'Товаров: {Product.objects.count()}')
```

Выход из shell:
```python
exit()
```

## 🧪 Запуск тестов

### Юнит-тесты (pytest)

```bash
# Все тесты
pytest

# Тесты shop
pytest shop/tests.py

# С выводом покрытия
pytest --cov=shop --cov=users --cov=cart --cov=orders
```

### Нагрузочное тестирование (Locust)

```bash
locust -f locustfile.py --host=http://localhost:8000
```

Откройте: http://localhost:8089

## 🔧 Административная панель

1. Войдите: http://localhost:8000/admin
2. Логин: `admin`
3. Пароль: тот, что указали при создании superuser

Возможности:
- Управление товарами и категориями
- Просмотр и обработка заказов
- Модерация отзывов
- Управление пользователями

## 📝 Основные URL

| URL | Описание |
|-----|----------|
| `/` | Главная страница |
| `/products/` | Каталог товаров |
| `/product/<id>/<slug>/` | Детальная страница товара |
| `/cart/` | Корзина |
| `/orders/create/` | Оформление заказа |
| `/users/register/` | Регистрация |
| `/users/login/` | Вход |
| `/users/profile/` | Профиль |
| `/admin/` | Админ-панель |

## ❗ Решение проблем

### Ошибка: "No module named 'PIL'"
```bash
pip install Pillow
```

### Ошибка: "no such table"
```bash
python manage.py migrate
```

### Ошибка: CSRF verification failed
Убедитесь, что в формах есть `{% csrf_token %}`

### Медиа файлы не отображаются
- Убедитесь что `DEBUG = True`
- Проверьте настройки `MEDIA_URL` и `MEDIA_ROOT`

## 🚀 Готово!

Проект полностью настроен и готов к работе!

**Следующие шаги:**
1. Создайте несколько товаров через админ-панель
2. Зарегистрируйте тестового пользователя
3. Протестируйте добавление в корзину и оформление заказа
4. Оставьте отзыв на товар

Удачи! 🎉
