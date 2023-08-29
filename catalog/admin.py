from catalog.models import Category, Product
from django.contrib import admin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Product)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'category',)
    list_filter = ('category',)