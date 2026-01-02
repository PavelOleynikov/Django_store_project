from django.contrib import admin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "is_published", "views_count")
    # Фильтрация по дате создания и признаку публикации
    list_filter = ("created_at", "is_published")
    # Поиск по полям заголовок и содержимого
    search_fields = ("title", "content")
    fields = ("title", "content", "preview", "is_published", "views_count")
