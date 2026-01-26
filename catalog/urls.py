from django.urls import path

from catalog.apps import CatalogConfig
from . import views

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.CatalogListView.as_view(), name="home"),
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path("category/<int:pk>/", views.ProductsCategoryListView.as_view(), name="category_detail"),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    path("products/<int:pk>/", views.CatalogDetailView.as_view(), name="product_detail"),
    path("products/new/", views.CatalogCreateView.as_view(), name="product_new"),
    path("products/<int:pk>/edit/", views.CatalogUpdateView.as_view(), name="product_edit"),
    path("products/<int:pk>/delete/", views.CatalogDeleteView.as_view(), name="product_delete"),
    path("products/<int:pk>/unpublish/", views.ProductUnpublishView.as_view(), name="product_unpublish"),
]
