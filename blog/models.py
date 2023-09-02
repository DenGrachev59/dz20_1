from django.db import models
from django.urls import reverse

NULLABLE = {'blank': True, 'null': True}


class Public(models.Model):
    name = models.CharField(max_length=250, verbose_name='Наименование публикации')
    slug = models.CharField(max_length=200, verbose_name='слаг', **NULLABLE)
    description = models.TextField(**NULLABLE, verbose_name='Содержание публикации')
    image = models.ImageField(upload_to='blog/%Y/%m/%d', **NULLABLE, verbose_name='Превью')
    available = models.BooleanField(default=True, verbose_name='опубликовано')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', **NULLABLE)
    update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name="просмотры")

    def __str__(self):
        return f'{self.name} ({self.description})'

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'
