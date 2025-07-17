from typing import List, Optional

from ninja import NinjaAPI, Schema
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


@api.get('/foodproducts/', response=List[FoodProductSchema])
@paginate
def list_food_products(request):
    return FoodProduct.objects.all()
