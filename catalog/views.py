from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product


class OwnerRequiredMixin:
    """Миксин для проверки, что пользователь - владелец продукта"""

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()

        # Проверяем, является ли пользователь владельцем
        if product.owner != request.user:
            return redirect("catalog:product_detail", pk=product.pk)

        return super().dispatch(request, *args, **kwargs)


class OwnerOrModeratorRequiredMixin:
    """Миксин для проверки, что пользователь - владелец или имеет право на удаление"""

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()

        # Владелец ИЛИ пользователь с правом can_delete_product (модератор)
        is_owner = product.owner == request.user
        is_moderator = request.user.has_perm("catalog.can_delete_product")

        if not (is_owner or is_moderator):
            return redirect("catalog:product_detail", pk=product.pk)

        return super().dispatch(request, *args, **kwargs)


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер для отмены публикации продукта"""

    model = Product
    permission_required = "catalog.can_unpublish_product"
    fields = []
    template_name = "catalog/product_unpublish.html"

    def form_valid(self, form):
        self.object.status = "unpublic"
        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        """После отмены публикации перенаправляем на страницу продукта"""

        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})


class CatalogListView(ListView):
    """Контроллер главной страницы"""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        # СУПЕРПОЛЬЗОВАТЕЛЬ видит ВСЕ продукты
        if self.request.user.is_superuser:
            return Product.objects.all()

        # МОДЕРАТОРЫ (с правами) видят ВСЕ продукты
        if self.request.user.is_authenticated and (
            self.request.user.has_perm("catalog.can_unpublish_product")
            or self.request.user.has_perm("catalog.can_delete_product")
        ):
            return Product.objects.all()

        # ОБЫЧНЫЙ АВТОРИЗОВАННЫЙ пользователь видит только опубликованные продукты
        if self.request.user.is_authenticated:
            return Product.objects.filter(status="public")

        # НЕАВТОРИЗОВАННЫЙ пользователь видит только опубликованные
        return Product.objects.filter(status="public")

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


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
    """Контроллер для отображения детальной информации о продукте"""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        # Разрешаем просмотр только опубликованных продуктов
        # или если пользователь является модератором
        if self.request.user.is_authenticated and (
            self.request.user.has_perm("catalog.can_unpublish_product")
            or self.request.user.has_perm("catalog.can_delete_product")
        ):
            return Product.objects.all()
        return Product.objects.filter(status="public")


class CatalogCreateView(LoginRequiredMixin, CreateView):
    """Создание нового продукта"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        product = form.save(commit=False)
        product.owner = self.request.user  # Назначаем текущего пользователя владельцем
        return super().form_valid(form)


class CatalogUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    """Редактирование продукта"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self):
        """После редактирования перенаправляем на страницу продукта"""

        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})


class CatalogDeleteView(LoginRequiredMixin, OwnerOrModeratorRequiredMixin, DeleteView):
    """Удаление продукта - для владельца или модератора"""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")
