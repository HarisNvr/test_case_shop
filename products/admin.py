from django.contrib import admin

from .models import (
    Category, SubCategory, Product, ShoppingCart
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'subcategory_count',
        'product_count'
    )
    list_filter = ('name', 'slug')


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'parent_category',
        'product_count'
    )
    list_filter = ('name', 'slug', 'parent_category')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'price',
        'subcategory'
    )
    list_filter = ('name', 'slug', 'price', 'subcategory')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product',
        'quantity',
        'product_price',
        'total_price'
    )
    list_filter = ('user', 'product')