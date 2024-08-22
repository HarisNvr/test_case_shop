from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from products.models import Category, SubCategory, Product


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name', 'slug', 'image', 'subcategory_count', 'product_count'
        )


class SubCategorySerializer(ModelSerializer):
    parent_category = SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = (
            'name', 'slug', 'image', 'parent_category', 'product_count'
        )

    def get_parent_category(self, obj):
        return obj.parent_category.name if obj.parent_category else None


class ProductSerializer(ModelSerializer):
    category = SerializerMethodField()
    subcategory = SerializerMethodField()
    images = SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'name', 'slug', 'category', 'subcategory', 'price', 'images'
        )

    def get_category(self, obj):
        return obj.category.name if obj.category else None

    def get_subcategory(self, obj):
        return obj.subcategory.name if obj.subcategory else None

    def get_images(self, obj):
        return {
            'small': obj.image_small.url if obj.image_small else None,
            'medium': obj.image_medium.url if obj.image_medium else None,
            'large': obj.image_large.url if obj.image_large else None,
        }
