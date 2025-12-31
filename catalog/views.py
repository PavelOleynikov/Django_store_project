from typing import Any

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from catalog.models import Product


def home(request: Any) -> HttpResponse:
    """Контроллер главной страницы"""

    products = Product.objects.all()
    context = {"products": products, "title": "Skystore - Главная"}
    return render(request, "catalog/home.html", context)


def contacts(request: Any) -> HttpResponse:
    """Контроллер страницы контактов"""

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        return HttpResponse(f"Спасибо, {name}! Сообщение получено.")
    return render(request, "catalog/contacts.html")


def product_detail(request: Any, pk: Any) -> HttpResponse:
    """Контроллер для отображения детальной информации о товаре"""

    product = get_object_or_404(Product, pk=pk)  # функция для получения объекта по pk, если не найден - raises 404
    context = {"product": product, "title": f"{product.name} - Детальная информация"}
    return render(request, "catalog/product_detail.html", context)
