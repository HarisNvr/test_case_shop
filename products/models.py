from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from .constants import (
    CATEGORY_NAME_LEN, CATEGORY_SLUG_LEN, SUBCATEGORY_NAME_LEN,
    SUBCATEGORY_SLUG_LEN, PRODUCT_NAME_LEN, PRODUCT_SLUG_LEN, PRICE_MAX,
    PRICE_LEN, SHOPPING_CART_MAX
)


class Category(models.Model):
    name = models.CharField(
        'Название',
        unique=True,
        max_length=CATEGORY_NAME_LEN
    )
    slug = models.SlugField(
        'Уникальный слаг',
        unique=True,
        max_length=CATEGORY_SLUG_LEN
    )
    image = models.ImageField(
        'Изображение',
        upload_to='categories/'
    )

    def subcategory_count(self):
        return self.subcategories.count()
    subcategory_count.short_description = 'Количество подкатегорий в категории'

    def product_count(self):
        return Product.objects.filter(
            subcategory__parent_category=self
        ).count()
    product_count.short_description = 'Количество продуктов в категории'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(
        'Название',
        unique=True,
        max_length=SUBCATEGORY_NAME_LEN
    )
    slug = models.SlugField(
        'Уникальный слаг',
        unique=True,
        max_length=SUBCATEGORY_SLUG_LEN
    )
    image = models.ImageField(
        'Изображение',
        upload_to='sub_categories/'
    )
    parent_category = models.ForeignKey(
        Category,
        verbose_name='Родительская категория',
        null=True,
        related_name='subcategories',
        on_delete=models.SET_NULL
    )

    def product_count(self):
        return self.products.count()
    product_count.short_description = 'Количество продуктов в подкатегории'

    class Meta:
        verbose_name = 'подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Название', max_length=PRODUCT_NAME_LEN)
    slug = models.SlugField(
        'Уникальный слаг',
        unique=True,
        max_length=PRODUCT_SLUG_LEN
    )
    price = models.DecimalField(
        'Цена',
        max_digits=PRICE_LEN,
        decimal_places=2,
        validators=[
            MinValueValidator(
                0,
                message=f'Минимальное значение {0}!'
            ),
            MaxValueValidator(
                PRICE_MAX,
                message=f'Максимальное значение {PRICE_MAX}!'
            )
        ]
    )
    image_small = models.ImageField(
        'Изображение',
        upload_to='products/small/'
    )
    image_medium = models.ImageField(
        'Изображение',
        upload_to='products/medium/'
    )
    image_large = models.ImageField(
        'Изображение',
        upload_to='products/large/'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='products',
        null=True,
        on_delete=models.SET_NULL,
        editable=False
    )
    subcategory = models.ForeignKey(
        SubCategory,
        verbose_name='Подкатегория',
        related_name='products',
        null=True,
        on_delete=models.SET_NULL
    )

    def save(self, *args, **kwargs):
        if self.subcategory:
            self.category = self.subcategory.parent_category
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-id']
        verbose_name = 'продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    quantity = models.DecimalField(
        verbose_name='Кол-во',
        max_digits=PRICE_LEN,
        decimal_places=1,
        validators=[
            MinValueValidator(
                0,
                message=f'Минимальное значение {0}!'
            ),
            MaxValueValidator(
                SHOPPING_CART_MAX,
                message=f'Максимальное значение {SHOPPING_CART_MAX}!'
            )
        ]
    )

    def product_price(self):
        return self.product.price
    product_price.short_description = 'Цена'

    def total_price(self):
        return self.product.price * self.quantity
    total_price.short_description = 'Сумма'

    class Meta:
        default_related_name = 'shopping_cart'
        verbose_name = 'ячейку корзины'
        verbose_name_plural = 'Корзина покупок пользователей'
        constraints = [
            UniqueConstraint(
                fields=['user', 'product'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return (
            f'Ячейка корзины {self.user.username}'
            f' с продуктом  "{self.product}"'
        )
