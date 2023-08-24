from django.core.management import BaseCommand

from catalog.models import Product, Category
from datetime import date


class Command(BaseCommand):

    def handle(self,  *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()

        category_list = [
            {'name': 'Телевизоры'},
            {'name': 'Музыкальные центры'},
            {'name': 'Плееры'},
            {'name': 'Ноутбуки'},
        ]

        for category_item in category_list:
            Category.objects.create(**category_item)

        category_tv = Category.objects.get(name='Телевизоры')
        category_mc = Category.objects.get(name='Музыкальные центры')
        category_pleer = Category.objects.get(name='Плееры')
        category_nb = Category.objects.get(name='Ноутбуки')


        product_list = [
            {'name': 'Фунай',
             'description': 'телевизор 55 дюймов',
             "photo": '',
             "category": category_tv,
             "price": 100000,
             "date_make": "2023-08-12",
             "date_update": "2023-08-20"},
            {'name': 'Сони',
             'description': 'музыкальный центр с радио и дисками',
             "photo": '',
             "category": category_mc,
             "price": 10000,
             "date_make": "2023-08-01",
             "date_update": "2023-08-15"},
            {'name': 'Dell',
             'description': 'yjen,er 16/256',
             "photo": '',
             "category": category_nb,
             "price": 75000,
             "date_make": "2023-06-24",
             "date_update": "2023-08-13"},

        ]


        for product_item in product_list:
            Product.objects.create(**product_item)



