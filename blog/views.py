from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import BlogPost


class BlogPostListView(ListView):
    """Список блоговых записей"""

    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "posts"


class BlogPostDetailView(DetailView):
    """Детальная информация о блоговой записи"""

    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "post"


class BlogPostCreateView(CreateView):
    """Создание новой блоговой записи"""

    model = BlogPost
    template_name = "blog/blogpost_form.html"
    context_object_name = "post"
    success_url = reverse_lazy("blog:post_list")


class BlogPostUpdateView(UpdateView):
    """Редактирование блоговой записи"""

    model = BlogPost
    template_name = "blog/blogpost_form.html"
    context_object_name = "post"
    success_url = reverse_lazy("blog:post_list")


class BlogPostDeleteView(DeleteView):
    """Удаление блоговой записи"""

    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
