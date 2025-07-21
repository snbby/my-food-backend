import pytest

from django.contrib.auth import get_user_model
from django.test import Client
from myfood.tests.factories import FoodProductFactory


@pytest.mark.django_db
def test_drf_pagination():
    FoodProductFactory.create_batch(100)
    client = Client()
    response = client.get('/drf/foodproducts/search/')
    data = response.json()
    assert len(data['items']) == 30
    assert 'count' not in data


@pytest.mark.django_db
def test_drf_search_food_products_q_param():
    FoodProductFactory.create_batch(5, product_name="eggs")
    FoodProductFactory.create_batch(3, product_name="Eggs Benedict")
    FoodProductFactory.create_batch(10, product_name="milk")
    client = Client()
    response = client.get('/drf/foodproducts/search/', data={'q': 'eggs'})
    data = response.json()
    product_names = [item['product_name'] for item in data['items']]
    for name in product_names:
        assert 'eggs' in name.lower()


@pytest.mark.django_db
def test_drf_search_detailed_food_products_auth():
    FoodProductFactory.create_batch(12)
    client = Client()
    # Unauthenticated request should return 403
    response = client.get('/drf/foodproducts/search_detailed/')
    assert response.status_code == 403

    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpass')
    client.login(username='testuser', password='testpass')
    response = client.get('/drf/foodproducts/search_detailed/')
    assert response.status_code == 200
    data = response.json()
    for item in data['items']:
        assert 'fiber_100g' in item
        assert 'sugars_100g' in item
