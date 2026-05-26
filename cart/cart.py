"""
Класс корзины для работы с сессиями.
Использует ООП принципы для управления состоянием корзины.
"""
from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:
    """
    Класс корзины покупок.
    Хранит товары в сессии пользователя.
    """
    
    def __init__(self, request):
        """
        Инициализация корзины.
        Получает или создает корзину в сессии.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        
        if not cart:
            # Создаем пустую корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart
    
    def add(self, product, quantity=1, override_quantity=False):
        """
        Добавить товар в корзину или обновить его количество.
        
        Args:
            product: Объект Product
            quantity: Количество товара
            override_quantity: Заменить количество или добавить
        """
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()
    
    def save(self):
        """
        Сохранить корзину в сессии.
        Помечает сессию как "измененную".
        """
        self.session.modified = True
    
    def remove(self, product):
        """
        Удалить товар из корзины.
        
        Args:
            product: Объект Product или ID товара
        """
        product_id = str(product.id if isinstance(product, Product) else product)
        
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        """
        Итерация по товарам в корзине.
        Получает товары из базы данных.
        """
        product_ids = self.cart.keys()
        
        # Получаем товары из БД
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """
        Подсчет общего количества товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """
        Подсчет общей стоимости товаров в корзине.
        """
        return sum(
            Decimal(item['price']) * item['quantity'] 
            for item in self.cart.values()
        )
    
    def clear(self):
        """
        Очистить корзину.
        Удаляет корзину из сессии.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
    
    def get_product_ids(self):
        """
        Получить список ID товаров в корзине.
        """
        return [int(product_id) for product_id in self.cart.keys()]
    
    def update_quantity(self, product_id, quantity):
        """
        Обновить количество товара в корзине.
        
        Args:
            product_id: ID товара
            quantity: Новое количество
        """
        product_id = str(product_id)
        
        if product_id in self.cart:
            if quantity > 0:
                self.cart[product_id]['quantity'] = quantity
            else:
                # Если количество 0 или меньше, удаляем товар
                del self.cart[product_id]
            
            self.save()
            return True
        
        return False
