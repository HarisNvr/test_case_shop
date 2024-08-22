from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, SubCategoryViewSet, ProductCategoryViewSet

app_name = 'api'

router = DefaultRouter()

router.register('categories', CategoryViewSet)
router.register('sub_categories', SubCategoryViewSet)
router.register('products', ProductCategoryViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
