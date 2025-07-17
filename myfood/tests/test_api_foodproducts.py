import pytest
from django.test import Client
from django.conf import settings

from myfood.tests.factories import FoodProductFactory

@pytest.mark.django_db
def test_pagination():
    batch = 1000
    FoodProductFactory.create_batch(batch)
    client = Client()

    # Testing default pagination from NINJA_PAGINATION_PER_PAGE setting
    response = client.get(
        path='/api/foodproducts/search/',
        content_type='application/json',
    )
    data = response.json()
    assert len(data['items']) == settings.NINJA_PAGINATION_PER_PAGE
    assert data['count'] == batch

    # Testing custom limit
    limit = 30
    response = client.get(
        path='/api/foodproducts/search/',
        content_type='application/json',
        data={'limit': limit}
    )
    data = response.json()
    assert len(data['items']) == limit

@pytest.mark.django_db
def test_search_food_products_q_param():
    # Create products with and without 'eggs' in the name
    FoodProductFactory.create_batch(5, product_name="eggs")
    FoodProductFactory.create_batch(3, product_name="Eggs Benedict")
    FoodProductFactory.create_batch(10, product_name="milk")
    client = Client()

    response = client.get(
        path='/api/foodproducts/search/',
        data={'q': 'eggs'},
        content_type='application/json',
    )
    data = response.json()
    # All items with 'eggs' (case-insensitive) in product_name should be returned
    assert data['count'] == 8
    product_names = [item['product_name'] for item in data['items']]
    for name in product_names:
        assert 'eggs' in name.lower()
