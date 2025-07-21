import pytest

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client
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

@pytest.mark.django_db
def test_search_detailed_food_products_auth():
    # Create some products
    batch = 12
    FoodProductFactory.create_batch(batch)
    client = Client()

    # 1. Unauthenticated request should return 401
    response = client.get(
        path='/api/foodproducts/search_detailed/',
        content_type='application/json',
    )
    assert response.status_code == 401

    # 2. Authenticated request should return default number of items
    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')
    response = client.get(
        path='/api/foodproducts/search_detailed/',
        content_type='application/json',
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) == min(settings.NINJA_PAGINATION_PER_PAGE, batch)
    # Check that two additional fields are present in each item
    for item in data['items']:
        assert 'fiber_100g' in item
        assert 'sugars_100g' in item