from rest_framework import serializers

from myfood.models import FoodProduct

class FoodProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodProduct
        fields = FoodProduct.api_fields