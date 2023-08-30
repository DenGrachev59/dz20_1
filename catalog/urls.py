from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import index, categories, category_products,product_desc

app_name = CatalogConfig.name

urlpatterns = [
    path('', index,name='index'),
    path('categories/', categories, name='categories'),
    path('<int:pk>/catalog/', category_products, name='category_products'),
    path('<int:pk>/product/', product_desc, name='product_desc')

]