"""
Нагрузочное тестирование с помощью Locust.

Запуск:
locust -f locustfile.py --host=http://localhost:8000

Открыть в браузере: http://localhost:8089
"""
from locust import HttpUser, task, between
import random


class ShopUser(HttpUser):
    """
    Симуляция поведения пользователя в интернет-магазине.
    """
    wait_time = between(1, 5)  # Пауза между запросами 1-5 секунд
    
    def on_start(self):
        """Выполняется при старте пользователя"""
        # Симуляция входа в систему
        self.client.post('/users/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
    
    @task(10)
    def view_homepage(self):
        """Просмотр главной страницы (наиболее частая операция)"""
        self.client.get('/')
    
    @task(8)
    def view_products(self):
        """Просмотр списка товаров"""
        self.client.get('/products/')
    
    @task(6)
    def view_product_detail(self):
        """Просмотр детальной страницы товара"""
        # Симуляция просмотра случайного товара
        product_id = random.randint(1, 10)
        self.client.get(f'/product/{product_id}/test-product/')
    
    @task(5)
    def search_products(self):
        """Поиск товаров"""
        search_terms = ['процессор', 'видеокарта', 'память', 'intel', 'amd']
        query = random.choice(search_terms)
        self.client.get(f'/products/?q={query}')
    
    @task(4)
    def view_category(self):
        """Просмотр товаров по категории"""
        categories = ['processors', 'videocards', 'ram', 'motherboards']
        category = random.choice(categories)
        self.client.get(f'/category/{category}/')
    
    @task(3)
    def add_to_cart(self):
        """Добавление товара в корзину"""
        product_id = random.randint(1, 10)
        self.client.post(f'/cart/add/{product_id}/', {
            'quantity': 1,
            'override': False
        })
    
    @task(2)
    def view_cart(self):
        """Просмотр корзины"""
        self.client.get('/cart/')
    
    @task(1)
    def add_to_wishlist(self):
        """Добавление в список желаний"""
        product_id = random.randint(1, 10)
        self.client.post(f'/wishlist/add/{product_id}/')
    
    @task(1)
    def view_profile(self):
        """Просмотр профиля"""
        self.client.get('/users/profile/')


class AdminUser(HttpUser):
    """
    Симуляция администратора.
    """
    wait_time = between(2, 10)
    
    def on_start(self):
        """Вход как администратор"""
        self.client.post('/users/login/', {
            'username': 'admin',
            'password': 'admin123'
        })
    
    @task(5)
    def view_admin_panel(self):
        """Просмотр админ-панели"""
        self.client.get('/admin/')
    
    @task(3)
    def view_orders(self):
        """Просмотр заказов"""
        self.client.get('/admin/orders/order/')
    
    @task(2)
    def view_products_admin(self):
        """Просмотр товаров в админке"""
        self.client.get('/admin/shop/product/')


class APIUser(HttpUser):
    """
    Симуляция пользователя API.
    """
    wait_time = between(0.5, 2)
    
    @task(10)
    def search_autocomplete(self):
        """Автодополнение поиска"""
        query = random.choice(['процессор', 'intel', 'amd', 'видео'])
        self.client.get(f'/api/search-autocomplete/?q={query}')
    
    @task(5)
    def wishlist_operations(self):
        """Операции со списком желаний"""
        product_id = random.randint(1, 10)
        if random.choice([True, False]):
            self.client.post(f'/wishlist/add/{product_id}/')
        else:
            self.client.post(f'/wishlist/remove/{product_id}/')
    
    @task(3)
    def cart_operations(self):
        """Операции с корзиной"""
        product_id = random.randint(1, 10)
        action = random.choice(['add', 'remove', 'update'])
        
        if action == 'add':
            self.client.post(f'/cart/add/{product_id}/', {
                'quantity': random.randint(1, 3)
            })
        elif action == 'remove':
            self.client.post(f'/cart/remove/{product_id}/')
        else:
            self.client.post(f'/cart/update/{product_id}/', {
                'quantity': random.randint(1, 5)
            })
