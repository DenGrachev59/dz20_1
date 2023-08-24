from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    # created_at = models.CharField(**NULLABLE, max_length=100, verbose_name='created_at')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name='Наименование продукта')
    description = models.TextField(**NULLABLE, verbose_name='Описание продукта')
    photo = models.ImageField(upload_to='product/', **NULLABLE, verbose_name='Фото продукта')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена')
    date_make = models.DateField(verbose_name='Дата создания')
    date_update = models.DateField(verbose_name='Дата изменения')

    def __str__(self):
        return f'{self.name} ({self.category})'


    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
