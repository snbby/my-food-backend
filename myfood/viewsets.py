import json

from rest_framework import viewsets, filters, response

from myfood.models import FoodProduct
from myfood.serializers import FoodProductSerializer

class FoodProductViewSet(viewsets.ModelViewSet):
    # http://127.0.0.1/api/foodproducts/?offset=0&limit=10&
    # filters=[{"id":"brands","value":"Mercadona"},{"id":"product_name","value":"Huevos"}]&
    # ordering=[{"id":"product_name","desc":false}]&
    # search
    http_method_names = ['get']
    serializer_class = FoodProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product_name', 'brands']
    
    def get_queryset(self):
        # queryset_filter = {}

        # filters = self.request.query_params.get('filters')
        # if filters:
        #     filters = json.loads(filters)
        #     for column in filters:
        #         queryset_filter[column['id']] = column['value']

        # queryset = FoodProduct.objects.filter(**queryset_filter)
        return FoodProduct.objects.all()