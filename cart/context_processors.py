"""
Context processor для корзины.
Делает корзину доступной во всех шаблонах.
"""
from .cart import Cart


def cart(request):
    """
    Добавляет объект корзины в контекст всех шаблонов.
    """
    return {'cart': Cart(request)}
