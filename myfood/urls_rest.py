from django.urls import path, include
from rest_framework import routers

from myfood.viewsets import FoodProductViewSet

router = routers.DefaultRouter()
router.register('foodproducts', FoodProductViewSet, basename='FoodProducts')

urlpatterns = [
    path('', include(router.urls))
]