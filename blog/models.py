from django.db import models


class BlogPost(models.Model):
    """Класс для постов в блоге"""

    title = models.CharField(max_length=150, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")
    preview = models.ImageField(upload_to="previews/", verbose_name="Превью", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=False, verbose_name="Признак публикации")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Блоговая запись"
        verbose_name_plural = "Блоговые записи"
        ordering = ["-created_at"]  # сортировка по дате создания по убыванию
        db_table = "blogpost"

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=["views_count"])
