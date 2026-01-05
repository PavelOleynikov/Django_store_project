from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import BlogPost


class BlogPostListView(ListView):
    """Список опубликованных статей"""

    model = BlogPost
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Переопределяем метод для фильтрации опубликованных статей"""

        queryset = super().get_queryset()
        return queryset.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """Детальная информация об опубликованной записи"""

    model = BlogPost
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        """Переопределяем метод для увеличения счетчика просмотров"""

        obj = super().get_object(queryset)
        obj.increment_views()
        return obj


class BlogPostCreateView(CreateView):
    """Создание новой статьи"""

    model = BlogPost
    template_name = "blog/post_form.html"
    fields = ["title", "content", "preview", "is_published"]
    success_url = reverse_lazy("blog:post_list")


class BlogPostUpdateView(UpdateView):
    """Редактирование статьи"""

    model = BlogPost
    template_name = "blog/post_form.html"
    fields = ["title", "content", "preview", "is_published"]

    def get_success_url(self):
        """После редактирования перенаправляем на страницу статьи"""

        return reverse_lazy("blog:post_detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(DeleteView):
    """Удаление статьи"""

    model = BlogPost
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
