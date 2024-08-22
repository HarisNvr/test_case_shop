from rest_framework.viewsets import ReadOnlyModelViewSet

from api.pagination import ShopPagination
from api.serializers import (
    CategorySerializer, SubCategorySerializer, ProductSerializer
)
from products.models import Category, SubCategory, Product


class CategoryViewSet(ReadOnlyModelViewSet):
    pagination_class = ShopPagination
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get']


class SubCategoryViewSet(ReadOnlyModelViewSet):
    pagination_class = ShopPagination
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    http_method_names = ['get']


class ProductCategoryViewSet(ReadOnlyModelViewSet):
    pagination_class = ShopPagination
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get']
