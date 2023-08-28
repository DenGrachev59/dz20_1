from django.shortcuts import render

from catalog.models import Category, Product


def index(request):
    context = {
        'object_list': Category.objects.all()[:3],
        'title': 'Магазин электроники - Главная'
    }

    return render(request, 'catalog/index.html', context)

def categories (request):
    context = {
        'object_list': Category.objects.all(),
        'title': 'Магазин электроники - все наши категории тораров'
    }

    return render(request, 'catalog/categories.html', context)

def category_products (request, pk):
    category_item = Category.objects.get(pk=pk)
    context = {
        'object_list': Product.objects.filter(category_id=pk),
        'title': f'Магазин электроники - все наши товары в категории {category_item.name}'
    }

    return render(request, 'catalog/products.html', context)