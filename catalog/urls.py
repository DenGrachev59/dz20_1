from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import IndexView, CategoryListView, ProductListView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, ProductDetailView, toggle_activity

app_name = CatalogConfig.name

urlpatterns = [
    path('', IndexView.as_view(),name='index'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('catalog/<int:pk>/', ProductListView.as_view(), name='category'),
    path('catalog/create/', ProductCreateView.as_view(), name='product_create'),
    path('catalog/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('catalog/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('view/<int:pk>', ProductDetailView.as_view(), name='view'),
    path('activity/<int:pk>', toggle_activity, name='toggle_activity')
]