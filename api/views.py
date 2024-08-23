from decimal import Decimal

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from api.pagination import ShopPagination
from api.serializers import (
    CategorySerializer, SubCategorySerializer, ProductSerializer,
    ShoppingCartSerializer
)
from products.constants import SHOPPING_CART_MAX
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
    serializer_class = ShoppingCartSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        products = []
        total_cart_price = 0

        for item in data:
            products.append(item['products'][0])
            total_product_price = item['total_product_price']
            total_cart_price += total_product_price
        total_cart_price = round(total_cart_price, 2)

        return Response(
            {
                'products': products,
                'total_cart_price': total_cart_price,
                'count': len(data)}
        )

    def create(self, request, *args, **kwargs):
        context = {'request': request}
        data = {
            'user': request.user.id,
            'product': request.data.get('product'),
            'quantity': request.data.get('quantity')
        }

        serializer = ShoppingCartSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)

        try:
            instance = ShoppingCart.objects.get(
                user=request.user,
                product=request.data.get('product')
            )
            at_cart_now = instance.quantity
            instance.quantity += Decimal(request.data.get('quantity'))

            if instance.quantity > SHOPPING_CART_MAX:
                return Response(
                    {
                        'detail': f'Максимальное количество продукта в '
                                  f'корзине - {SHOPPING_CART_MAX}! '
                                  f'Вы можете добавить в корзину ещё не более '
                                  f'{SHOPPING_CART_MAX - at_cart_now}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            instance.save()
        except ShoppingCart.DoesNotExist:
            instance = ShoppingCart.objects.create(
                user=request.user,
                product=Product.objects.get(pk=request.data.get('product')),
                quantity=request.data.get('quantity')
            )

        serializer = self.get_serializer(instance)
        return Response(
            serializer.data['products'],
            status=status.HTTP_201_CREATED
        )

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = ShoppingCart.objects.get(
                user=request.user,
                product=kwargs.get('pk')
            )
        except ShoppingCart.DoesNotExist:
            raise NotFound({'detail': 'Товар не найден в корзине.'})

        quantity = request.data.get('quantity')
        if quantity is None:
            return Response(
                {'detail': 'Необходимо указать количество.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        quantity = Decimal(quantity)

        if quantity <= 0:
            return Response(
                {'detail': 'Количество должно быть больше 0.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if quantity > SHOPPING_CART_MAX:
            return Response(
                {
                    'detail': f'Максимальное количество продукта '
                              f'в корзине - {SHOPPING_CART_MAX}.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.quantity = quantity
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = ShoppingCart.objects.get(
                user=request.user,
                product=kwargs.get('pk')
            )
        except ShoppingCart.DoesNotExist:
            raise NotFound({'detail': 'Товар не найден в корзине.'})

        self.perform_destroy(instance)
        return Response(
            {f'detail': 'Продукт удалён из корзины.'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['delete'], url_path='clear')
    def destroy_all(self, request):
        ShoppingCart.objects.filter(user=request.user).delete()
        return Response(
            {'detail': 'Корзина очищена.'},
            status=status.HTTP_204_NO_CONTENT
        )
