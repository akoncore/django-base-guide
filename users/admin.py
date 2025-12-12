from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Shop

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('role', 'phone', 'avatar')}),
    )

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'owner__username']
    prepopulated_fields = {'slug': ('name',)}