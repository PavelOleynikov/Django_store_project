from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product


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

        if self.request.user.is_authenticated and (
            self.request.user.has_perm("catalog.can_unpublish_product")
            or self.request.user.has_perm("catalog.can_delete_product")
        ):

            return Product.objects.all()
        return Product.objects.filter(status="public")


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


class CatalogUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование продукта"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self):
        """После редактирования перенаправляем на страницу продукта"""

        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})


class CatalogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление продукта - только для модераторов"""

    model = Product
    permission_required = "catalog.can_delete_product"
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")
