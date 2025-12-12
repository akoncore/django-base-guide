from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Клиент'),
        ('seller', 'Продавец'),
        ('admin', 'Администратор'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Shop(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop', limit_choices_to={'role': 'seller'})
    name = models.CharField(max_length=200, unique=True, verbose_name='Название магазина')
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    logo = models.ImageField(upload_to='shops/logos/', blank=True, null=True, verbose_name='Логотип')
    banner = models.ImageField(upload_to='shops/banners/', blank=True, null=True, verbose_name='Баннер')
    address = models.CharField(max_length=300, blank=True, verbose_name='Адрес')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("main:shop_detail", args=[self.slug])
    
    def total_products(self):
        return self.products.filter(available=True).count()
    
    def total_sold(self):
        from orders.models import OrderItem
        return OrderItem.objects.filter(product__shop=self).count()
    
    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ['-created_at']