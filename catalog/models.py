from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование категории")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]  # сортировка по названию по умолчанию
        db_table = "category"  # название таблицы в базе данных


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование продукта")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to="images/", verbose_name="Изображение", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="products", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за покупку")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")
    PUBLIC_STATUS = [("public", "Опубликовано"), ("unpublic", "Не опубликовано")]
    status = models.CharField(
        max_length=25,
        choices=PUBLIC_STATUS,
        default="unpublic",
        verbose_name="Статус публикации",
    )

    def __str__(self):
        return f"{self.name} {self.category} {self.price}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["created_at", "category"]
        db_table = "products"
        permissions = [
            ("can_unpublish_product", "Право отменять публикацию продукта"),
            ("can_delete_product", "Право на удаление любого продукта"),
        ]
