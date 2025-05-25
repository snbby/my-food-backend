from django.urls import path, include
from rest_framework import routers

from myfood.viewsets import FoodProductViewSet, SensorDataViewSet

router = routers.DefaultRouter()
router.register('foodproducts', FoodProductViewSet, basename='FoodProducts')
router.register('sensor-data', SensorDataViewSet, basename='sensor-data')

urlpatterns = [
    path('', include(router.urls))
]