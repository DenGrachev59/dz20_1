from django.conf import settings
from django.db import models
from django.urls import reverse

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    slug = models.SlugField(max_length=200, unique=True,verbose_name='Слап', **NULLABLE)
    # created_at = models.CharField(**NULLABLE, max_length=100, verbose_name='created_at')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('catalog: product_list_by_category',args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name='Наименование продукта')
    slug = models.SlugField(max_length=200, verbose_name='Слаг',**NULLABLE)
    description = models.TextField(**NULLABLE, verbose_name='Описание продукта')
    image = models.ImageField(upload_to='product/%Y/%m/%d', **NULLABLE, verbose_name='Фото продукта')
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    available = models.BooleanField(default=True,verbose_name='опубликовано')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', **NULLABLE)
    update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name="просмотры")

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return f'{self.name} ({self.category})'


    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def get_absolutle_url(self):
        return reverse('catalog:product_detail', args=[self.id, self.slug])


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="продукт")
    number = models.IntegerField( verbose_name='номер версии')
    name = models.CharField(max_length=250, verbose_name='название версии')
    available = models.BooleanField(default=True,verbose_name='активность версии')

    def __str__(self):
        return f'{self.number} ({self.name})'


    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
