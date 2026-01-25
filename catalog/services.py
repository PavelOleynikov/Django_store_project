from django.core.cache import cache

from catalog.models import Product, Category
from config.settings import CACHE_ENABLED


def get_all_categories():
    """Получение всех категорий"""

    return Category.objects.all()


def get_products_by_category(category_pk):
    """Получение продуктов по категории"""

    return Product.objects.filter(category_id=category_pk)


def get_products_from_cache():
    """Получаем список продуктов из кеша или БД"""

    if not CACHE_ENABLED:
        return Product.objects.all()
    key = "products_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products
