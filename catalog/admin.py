from catalog.models import Category, Product, Version
from django.contrib import admin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Product)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'category',)
    list_filter = ('category',)

@admin.register(Version)
class VesionAdmin(admin.ModelAdmin):
    list_display = ('product', 'number', 'name', 'available',)
    list_filter = ('product', 'number', 'name', 'available',)

