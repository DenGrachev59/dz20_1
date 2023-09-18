from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABLE

class User(AbstractUser):

    DoesNotExist = None
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=150, verbose_name='страна', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='автатар', **NULLABLE)

    is_active = models.BooleanField(default=False, verbose_name='активность', **NULLABLE )
    register_uuid = models.CharField(max_length=50, **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
