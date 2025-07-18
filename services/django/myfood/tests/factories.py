import factory
from faker import Faker

from myfood.models import FoodProduct

fake = Faker()

class FoodProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FoodProduct

    product_name = factory.LazyAttribute(lambda x: fake.word().capitalize())
    brands = factory.Faker('company')
    countries = factory.Faker('country')
    fat_100g = factory.Faker('pyfloat', left_digits=2, right_digits=1, min_value=0, max_value=50)
    carbohydrates_100g = factory.Faker('pyfloat', left_digits=2, right_digits=1, min_value=0, max_value=100)
    proteins_100g = factory.Faker('pyfloat', left_digits=2, right_digits=1, min_value=0, max_value=50)
