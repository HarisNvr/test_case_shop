from rest_framework.pagination import PageNumberPagination

from products.constants import PAGE_SIZE


class ShopPagination(PageNumberPagination):
    page_size = PAGE_SIZE
    page_size_query_param = 'limit'
