from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from api.pagination import ShopPagination
from api.serializers import (
    CategorySerializer, SubCategorySerializer, ProductSerializer,
    ShoppingCartSerializer
)
from products.models import Category, SubCategory, Product, ShoppingCart
from .permissions import IsAuthor


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


class ShoppingCartViewSet(ModelViewSet):
    queryset = ShoppingCart.objects.all()
    permission_classes = (IsAuthor,)
    pagination_class = ShopPagination
    serializer_class = ShoppingCartSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        products = []

        for item in data['results']:
            products.append(item['products'])

        return Response({'products': products, 'count': data['count']})


