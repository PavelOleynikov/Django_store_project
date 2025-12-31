from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View

from catalog.models import Product


class CatalogListView(ListView):
    """Контроллер главной страницы"""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"


class ContactsView(View):
    """Контроллер страницы контактов"""

    def get(self, request):
        """Обработка GET запроса"""

        return render(request, "catalog/contacts.html")

    def post(self, request):
        """Обработка POST запроса"""

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        return HttpResponse(f"Спасибо, {name}! Сообщение получено.")


class CatalogDetailView(DetailView):
    """Контроллер для отображения детальной информации о товаре"""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

