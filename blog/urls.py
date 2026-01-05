from django.urls import path

from blog.apps import BlogConfig
from . import views

app_name = BlogConfig.name

urlpatterns = [
    path("", views.BlogPostListView.as_view(), name="post_list"),
    path("blogs/<int:pk>/", views.BlogPostDetailView.as_view(), name="post_detail"),
    path("blogs/new/", views.BlogPostCreateView.as_view(), name="post_create"),
    path("blogs/<int:pk>/edit/", views.BlogPostUpdateView.as_view(), name="post_update"),
    path("blogs/<int:pk>/delete/", views.BlogPostDeleteView.as_view(), name="post_delete"),
]
