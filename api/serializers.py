from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField, DecimalField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from products.constants import PRICE_LEN, SHOPPING_CART_MAX
from products.models import Category, SubCategory, Product, ShoppingCart


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


class ShoppingCartSerializer(ModelSerializer):
    products = SerializerMethodField()
    product = PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True
    )
    quantity = DecimalField(
        max_digits=PRICE_LEN,
        decimal_places=1,
        write_only=True
    )
    total_product_price = SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = (
            'products', 'product', 'quantity', 'product_price',
            'total_product_price'
        )
        read_only_fields = ('user',)

    def validate(self, data):
        quantity = data.get('quantity')

        if quantity <= 0:
            raise ValidationError(
                {'quantity': 'Количество должно быть больше 0!'})
        if quantity > SHOPPING_CART_MAX:
            raise ValidationError(
                {'quantity': f'Максимальное количество {SHOPPING_CART_MAX}!'})

        if quantity.as_tuple().exponent < -1:
            raise ValidationError(
                {'quantity': 'Количество может иметь не более '
                             'одного знака после запятой!'}
            )

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request is None:
            raise ValidationError({'detail': 'Необходим контекст запроса.'})

        user = request.user
        return ShoppingCart.objects.create(user=user, **validated_data)

    def get_total_product_price(self, obj):
        return obj.product.price * obj.quantity

    def get_products(self, obj):
        return [
            {
                'product': obj.product.name,
                'id': obj.product.id,
                'quantity': obj.quantity,
                'product_price': obj.product.price,
                'total_product_price': self.get_total_product_price(obj)
            }
        ]
