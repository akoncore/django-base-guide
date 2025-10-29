from django.contrib import admin
from .models import Category,Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}
    
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category','price','available','created_at','updated_at']
    list_flter = ['available','created_at','updated_at']
    list_editable = ['price','available']
    prepopulated_fields = {'slug':('name',)}
    