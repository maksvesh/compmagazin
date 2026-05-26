# Интернет-магазин компьютеров на Django

Полнофункциональный интернет-магазин компьютеров и комплектующих, разработанный на Django 5.0.

## 🚀 Особенности

- ✅ Каталог товаров с фильтрацией и поиском
- ✅ Корзина покупок (сессии)
- ✅ Система заказов
- ✅ Авторизация и регистрация
- ✅ Отзывы и рейтинги товаров
- ✅ Список желаний
- ✅ История просмотров
- ✅ Административная панель
- ✅ Защита от CSRF
- ✅ Загрузка изображений с валидацией
- ✅ Полное покрытие тестами

## 📋 Требования

- Python 3.10+
- Django 5.0.1
- Pillow 10.2.0
- PostgreSQL (опционально, по умолчанию SQLite)

## 🛠 Установка

### 1. Клонирование репозитория

```bash
git clone <repository_url>
cd computer_shop
```

### 2. Создание виртуального окружения

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка базы данных

#### Вариант A: SQLite (по умолчанию)

Не требует дополнительной настройки.

#### Вариант B: PostgreSQL

1. Создайте базу данных:
```sql
CREATE DATABASE computer_shop_db;
CREATE USER shop_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE computer_shop_db TO shop_user;
```

2. Обновите `computer_shop_project/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'computer_shop_db',
        'USER': 'shop_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Применение миграций

```bash
python manage.py migrate
```

### 6. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 7. Загрузка тестовых данных (опционально)

```bash
python manage.py loaddata fixtures/initial_data.json
```

### 8. Запуск сервера

```bash
python manage.py runserver
```

Откройте браузер: http://localhost:8000

## 📁 Структура проекта

```
computer_shop/
├── computer_shop_project/   # Главный проект
│   ├── settings.py          # Настройки
│   ├── urls.py              # Главный роутинг
│   └── wsgi.py              # WSGI конфигурация
├── shop/                    # Приложение магазина
│   ├── models.py            # Модели (Product, Category, Review)
│   ├── views.py             # Представления
│   ├── forms.py             # Формы
│   ├── urls.py              # URL маршруты
│   ├── admin.py             # Админ-панель
│   └── tests.py             # Тесты
├── users/                   # Приложение пользователей
│   ├── models.py            # UserProfile
│   ├── views.py             # Регистрация, вход
│   ├── forms.py             # Формы авторизации
│   └── urls.py              # URL маршруты
├── cart/                    # Приложение корзины
│   ├── cart.py              # Класс Cart
│   ├── views.py             # API корзины
│   ├── forms.py             # Формы корзины
│   └── urls.py              # URL маршруты
├── orders/                  # Приложение заказов
│   ├── models.py            # Order, OrderItem
│   ├── views.py             # Создание заказов
│   ├── forms.py             # Формы заказов
│   └── urls.py              # URL маршруты
├── templates/               # Шаблоны HTML
├── media/                   # Загруженные файлы
├── static/                  # Статические файлы
├── manage.py                # Django management
├── requirements.txt         # Зависимости
├── pytest.ini               # Конфигурация pytest
├── conftest.py              # Фикстуры для тестов
├── locustfile.py            # Нагрузочное тестирование
└── README.md                # Этот файл
```

## 🧪 Тестирование

### Юнит-тесты (pytest)

```bash
# Запуск всех тестов
pytest

# Запуск тестов конкретного приложения
pytest shop/tests.py

# С покрытием кода
pytest --cov=shop --cov=users --cov=cart --cov=orders
```

### Нагрузочное тестирование (Locust)

```bash
# Запуск Locust
locust -f locustfile.py --host=http://localhost:8000

# Откройте браузер: http://localhost:8089
# Настройте количество пользователей и начните тест
```

## 📝 API Эндпоинты

### Публичные
- `GET /` - Главная страница
- `GET /products/` - Каталог товаров
- `GET /products/?q=intel` - Поиск
- `GET /category/<slug>/` - Товары по категории
- `GET /product/<id>/<slug>/` - Детальная страница товара

### Корзина
- `GET /cart/` - Просмотр корзины
- `POST /cart/add/<id>/` - Добавить в корзину (JSON)
- `POST /cart/remove/<id>/` - Удалить из корзины (JSON)
- `POST /cart/update/<id>/` - Обновить количество (JSON)

### Пользователи
- `POST /users/register/` - Регистрация
- `POST /users/login/` - Вход
- `GET /users/logout/` - Выход
- `GET/POST /users/profile/` - Профиль (требует авторизации)

### Заказы (требует авторизации)
- `GET/POST /orders/create/` - Создать заказ
- `GET /orders/` - Список заказов
- `GET /orders/<id>/` - Детали заказа

### Список желаний (требует авторизации)
- `GET /wishlist/` - Список желаний
- `POST /wishlist/add/<id>/` - Добавить (JSON)
- `POST /wishlist/remove/<id>/` - Удалить (JSON)

## 🔒 Безопасность

Проект включает следующие меры безопасности:

- ✅ CSRF защита на всех формах
- ✅ Хеширование паролей (PBKDF2)
- ✅ HTTP-only cookies
- ✅ Валидация всех пользовательских вводов
- ✅ Защита от SQL-инъекций (Django ORM)
- ✅ Защита от XSS атак
- ✅ Ограничение размера загружаемых файлов
- ✅ Валидация типов файлов

## 📚 Документация

Полная документация проекта находится в файле `DOCUMENTATION.md` и включает:

1. Введение (актуальность, цели, задачи)
2. Анализ требований и проектирование архитектуры
3. Реализация системы авторизации и регистрации
4. Реализация загрузки файлов
5. Взаимодействие с базой данных
6. Тестирование
7. Заключение и перспективы развития

## 🎯 Основные модели

### Product (Товар)
- Название, описание, цена
- Категория, изображение
- Характеристики (JSON)
- Наличие, количество на складе
- Счетчик просмотров

### Category (Категория)
- Название, slug, описание
- Изображение

### Order (Заказ)
- Пользователь, статус
- Данные получателя
- Адрес доставки
- Товары (через OrderItem)

### Review (Отзыв)
- Товар, пользователь
- Рейтинг (1-5), комментарий
- Модерация

### UserProfile (Профиль)
- Расширение User
- Телефон, адрес
- Аватар

## 🔧 Администрирование

Доступ к админ-панели: http://localhost:8000/admin

Возможности:
- Управление товарами и категориями
- Просмотр и обработка заказов
- Модерация отзывов
- Управление пользователями
- Статистика и отчеты

## 📊 База данных

### Схема (основные таблицы)

- `shop_category` - Категории товаров
- `shop_product` - Товары
- `shop_productimage` - Дополнительные изображения
- `shop_review` - Отзывы на товары
- `shop_wishlist` - Списки желаний
- `shop_viewhistory` - История просмотров
- `users_userprofile` - Профили пользователей
- `orders_order` - Заказы
- `orders_orderitem` - Элементы заказов

## 🚀 Развертывание (Production)

### 1. Настройки безопасности

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
```

### 2. Сбор статических файлов

```bash
python manage.py collectstatic
```

### 3. Gunicorn + Nginx

```bash
# Установка Gunicorn
pip install gunicorn

# Запуск
gunicorn computer_shop_project.wsgi:application --bind 0.0.0.0:8000
```

### 4. PostgreSQL (рекомендуется)

Переключитесь на PostgreSQL для продакшена.

## 📝 Лицензия

Учебный проект. Свободное использование.

## 👨‍💻 Автор

Разработано как учебный проект для демонстрации навыков Django разработки.

## 🤝 Вклад

Pull requests приветствуются! Для больших изменений сначала откройте issue.

## 📧 Контакты

Для вопросов и предложений создайте issue в репозитории.
