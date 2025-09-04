from rest_framework import generics, permissions, serializers
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from drf_orjson_renderer.renderers import ORJSONRenderer


from django.db.models import QuerySet

from myfood.models import FoodProduct
from myfood.renderers import MsgspecJSONRenderer

class FoodPagination(LimitOffsetPagination):
    default_limit = 30
    max_limit = 100

    def get_paginated_response(self, data):
        return Response({
            'items': data,
            'next': self.get_next_link(),
            'prev': self.get_previous_link(),
        })


class FoodProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodProduct
        fields = ['id', 'product_name', 'brands', 'countries', 'fat_100g', 'carbohydrates_100g', 'proteins_100g']


class FoodProductDetailSerializer(FoodProductSerializer):
    class Meta(FoodProductSerializer.Meta):
        fields = FoodProductSerializer.Meta.fields + ['fiber_100g', 'sugars_100g']


class SearchFoodProducts(generics.ListAPIView):
    serializer_class = FoodProductSerializer
    pagination_class = FoodPagination

    def get_queryset(self) -> QuerySet:
        qs = FoodProduct.objects.all()
        q = self.request.query_params.get('q')
        if q:
            qs = qs.filter(product_name__icontains=q)
        return qs

class SearchDetailedFoodProducts(SearchFoodProducts):
    serializer_class = FoodProductDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class SearchFoodProductsOrJson(generics.ListAPIView):
    serializer_class = FoodProductSerializer
    pagination_class = FoodPagination
    renderer_classes = [ORJSONRenderer]

    def get_queryset(self) -> QuerySet:
        qs = FoodProduct.objects.all()
        q = self.request.query_params.get('q')
        if q:
            qs = qs.filter(product_name__icontains=q)
        return qs
    
class SearchFoodProductsMsgSpec(generics.ListAPIView):
    serializer_class = FoodProductSerializer
    pagination_class = FoodPagination
    renderer_classes = [MsgspecJSONRenderer]

    def get_queryset(self) -> QuerySet:
        qs = FoodProduct.objects.all()
        q = self.request.query_params.get('q')
        if q:
            qs = qs.filter(product_name__icontains=q)
        return qs