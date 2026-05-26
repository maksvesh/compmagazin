"""
Конфигурация и фикстуры для pytest.
"""
import pytest
from django.contrib.auth.models import User
from shop.models import Category, Product
from decimal import Decimal


@pytest.fixture
def create_user(db):
    """Фикстура для создания тестового пользователя"""
    def make_user(username='testuser', email='test@example.com', password='testpass123'):
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Test',
            last_name='User'
        )
    return make_user


@pytest.fixture
def user(create_user):
    """Базовый тестовый пользователь"""
    return create_user()


@pytest.fixture
def create_category(db):
    """Фикстура для создания категории"""
    def make_category(name='Процессоры', slug='processors'):
        return Category.objects.create(
            name=name,
            slug=slug,
            description=f'Категория {name}'
        )
    return make_category


@pytest.fixture
def category(create_category):
    """Базовая тестовая категория"""
    return create_category()


@pytest.fixture
def create_product(db, category):
    """Фикстура для создания товара"""
    def make_product(
        name='Intel Core i7',
        slug='intel-core-i7',
        price=25000,
        stock=10,
        available=True
    ):
        return Product.objects.create(
            category=category,
            name=name,
            slug=slug,
            price=Decimal(str(price)),
            stock=stock,
            available=available,
            description=f'Описание {name}',
            specifications={'cores': 8, 'threads': 16}
        )
    return make_product


@pytest.fixture
def product(create_product):
    """Базовый тестовый товар"""
    return create_product()


@pytest.fixture
def products(create_product):
    """Несколько тестовых товаров"""
    return [
        create_product(name='Intel Core i5', slug='intel-i5', price=15000),
        create_product(name='Intel Core i7', slug='intel-i7', price=25000),
        create_product(name='Intel Core i9', slug='intel-i9', price=35000),
    ]


@pytest.fixture
def client_with_user(client, user):
    """Клиент с авторизованным пользователем"""
    client.force_login(user)
    return client
