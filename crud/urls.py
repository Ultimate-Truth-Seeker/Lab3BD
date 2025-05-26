from django.urls import path
from .views import (
    ProductIndexListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)

urlpatterns = [
    path('products/',           ProductIndexListView.as_view(), name='product_list'),
    path('products/create/',    ProductCreateView.as_view(),    name='product_create'),
    path('products/<int:pk>/edit/',   ProductUpdateView.as_view(),    name='product_edit'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(),    name='product_delete'),
]