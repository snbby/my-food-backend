from typing import List, Optional

from ninja import NinjaAPI, Schema
# from ninja.security import django_auth
from ninja.pagination import paginate
from myfood.models import FoodProduct

api = NinjaAPI()

class FoodProductSchema(Schema):
    id: int
    product_name: Optional[str]
    brands: Optional[str]
    countries: Optional[str]
    fat_100g: Optional[float]
    carbohydrates_100g: Optional[float]
    proteins_100g: Optional[float]

# class FoodProductDetailSchema(FoodProductSchema):
#     fiber_100g: Optional[float]
#     sugars_100g: Optional[float]

@api.get('/foodproducts/search/', response=List[FoodProductSchema])
@paginate
def search_food_products(request, q: Optional[str] = None):
    qs = FoodProduct.objects.all()
    if q:
        qs = qs.filter(product_name__icontains=q)
    return qs

# @api.get('/foodproducts/search_detailed/', response=List[FoodProductSchema])
# @paginate
# def search_detailed_food_products(request, q: Optional[str] = None, auth=django_auth):
#     qs = FoodProduct.objects.all()
#     if q:
#         qs = qs.filter(product_name__icontains=q)
#     return qs