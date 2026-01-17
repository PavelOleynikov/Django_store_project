from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm
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


class CatalogDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для отображения детальной информации о товаре"""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class CatalogCreateView(LoginRequiredMixin, CreateView):
    """Создание нового продукта"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")


class CatalogUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование продукта"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self):
        """После редактирования перенаправляем на страницу продукта"""

        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})


class CatalogDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление продукта"""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")
