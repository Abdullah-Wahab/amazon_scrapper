from django.contrib import admin
from .models import Brand, Product

# Register your models here.


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'asin', 'sku', 'brand')
    search_fields = ('name', 'asin', 'sku')
