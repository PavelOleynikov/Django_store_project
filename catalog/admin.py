from django.contrib import admin

from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    # Фильтрация по категории
    list_filter = ('category',)
    # Поиск по полям name и description
    search_fields = ('name', 'description')