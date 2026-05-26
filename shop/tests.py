"""
Юнит-тесты для приложения магазина.
Тестирование моделей и представлений.
"""
import pytest
from django.urls import reverse
from decimal import Decimal
from shop.models import Category, Product, Review, Wishlist


@pytest.mark.django_db
class TestCategoryModel:
    """Тесты модели Category"""
    
    def test_category_creation(self, category):
        """Тест создания категории"""
        assert category.name == 'Процессоры'
        assert category.slug == 'processors'
        assert str(category) == 'Процессоры'
    
    def test_category_get_absolute_url(self, category):
        """Тест получения URL категории"""
        url = category.get_absolute_url()
        assert url == reverse('shop:product_list_by_category', args=[category.slug])


@pytest.mark.django_db
class TestProductModel:
    """Тесты модели Product"""
    
    def test_product_creation(self, product):
        """Тест создания товара"""
        assert product.name == 'Intel Core i7'
        assert product.price == Decimal('25000')
        assert product.stock == 10
        assert product.available is True
        assert str(product) == 'Intel Core i7'
    
    def test_product_get_absolute_url(self, product):
        """Тест получения URL товара"""
        url = product.get_absolute_url()
        assert url == reverse('shop:product_detail', args=[product.id, product.slug])
    
    def test_product_average_rating_no_reviews(self, product):
        """Тест среднего рейтинга без отзывов"""
        assert product.average_rating() == 0
    
    def test_product_average_rating_with_reviews(self, product, user, create_user):
        """Тест среднего рейтинга с отзывами"""
        Review.objects.create(product=product, user=user, rating=5, comment='Отлично', is_approved=True)
        user2 = create_user(username='user2', email='user2@example.com')
        Review.objects.create(product=product, user=user2, rating=3, comment='Неплохо', is_approved=True)
        
        # Средний рейтинг (5 + 3) / 2 = 4.0
        assert product.average_rating() == 4.0
    
    def test_product_increment_views(self, product):
        """Тест увеличения счетчика просмотров"""
        initial_views = product.views_count
        product.increment_views()
        product.refresh_from_db()
        assert product.views_count == initial_views + 1


@pytest.mark.django_db
class TestReviewModel:
    """Тесты модели Review"""
    
    def test_review_creation(self, product, user):
        """Тест создания отзыва"""
        review = Review.objects.create(
            product=product,
            user=user,
            rating=5,
            comment='Отличный товар!',
            is_approved=True
        )
        assert str(review) == f"Отзыв от {user.username} на {product.name}"
        assert review.rating == 5
        assert review.is_approved is True
    
    def test_review_unique_constraint(self, product, user):
        """Тест уникальности отзыва (один пользователь - один отзыв)"""
        Review.objects.create(product=product, user=user, rating=5, comment='Первый')
        
        with pytest.raises(Exception):
            Review.objects.create(product=product, user=user, rating=4, comment='Второй')


@pytest.mark.django_db
class TestWishlistModel:
    """Тесты модели Wishlist"""
    
    def test_wishlist_creation(self, product, user):
        """Тест добавления в список желаний"""
        wishlist_item = Wishlist.objects.create(user=user, product=product)
        assert str(wishlist_item) == f"{user.username} - {product.name}"
    
    def test_wishlist_unique_constraint(self, product, user):
        """Тест уникальности (один товар у пользователя один раз)"""
        Wishlist.objects.create(user=user, product=product)
        
        with pytest.raises(Exception):
            Wishlist.objects.create(user=user, product=product)


@pytest.mark.django_db
class TestProductListView:
    """Тесты представления списка товаров"""
    
    def test_product_list_view(self, client, products):
        """Тест отображения списка товаров"""
        url = reverse('shop:product_list')
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'products' in response.context
        assert len(response.context['products']) == 3
    
    def test_product_list_by_category(self, client, products, category):
        """Тест фильтрации по категории"""
        url = reverse('shop:product_list_by_category', args=[category.slug])
        response = client.get(url)
        
        assert response.status_code == 200
        assert response.context['category'] == category
    
    def test_product_search(self, client, products):
        """Тест поиска товаров"""
        url = reverse('shop:product_list')
        response = client.get(url, {'q': 'i7'})
        
        assert response.status_code == 200
        results = response.context['products']
        assert len(results) == 1
        assert 'i7' in results[0].name.lower()


@pytest.mark.django_db
class TestProductDetailView:
    """Тесты детального представления товара"""
    
    def test_product_detail_view(self, client, product):
        """Тест отображения детальной страницы товара"""
        url = product.get_absolute_url()
        response = client.get(url)
        
        assert response.status_code == 200
        assert response.context['product'] == product
    
    def test_product_detail_increments_views(self, client, product):
        """Тест увеличения просмотров при посещении"""
        initial_views = product.views_count
        url = product.get_absolute_url()
        client.get(url)
        
        product.refresh_from_db()
        assert product.views_count == initial_views + 1


@pytest.mark.django_db
class TestWishlistViews:
    """Тесты представлений списка желаний"""
    
    def test_add_to_wishlist_authenticated(self, client_with_user, product, user):
        """Тест добавления в список желаний для авторизованного пользователя"""
        url = reverse('shop:add_to_wishlist', args=[product.id])
        response = client_with_user.post(url)
        
        assert response.status_code == 200
        assert Wishlist.objects.filter(user=user, product=product).exists()
    
    def test_add_to_wishlist_unauthenticated(self, client, product):
        """Тест добавления в список желаний для неавторизованного пользователя"""
        url = reverse('shop:add_to_wishlist', args=[product.id])
        response = client.post(url)
        
        assert response.status_code == 401
    
    def test_remove_from_wishlist(self, client_with_user, product, user):
        """Тест удаления из списка желаний"""
        Wishlist.objects.create(user=user, product=product)
        
        url = reverse('shop:remove_from_wishlist', args=[product.id])
        response = client_with_user.post(url)
        
        assert response.status_code == 200
        assert not Wishlist.objects.filter(user=user, product=product).exists()
