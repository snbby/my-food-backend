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
        path='/api/foodproducts/',
        content_type='application/json',
    )
    data = response.json()
    assert len(data['items']) == settings.NINJA_PAGINATION_PER_PAGE
    assert data['count'] == batch

    # Testing custom limit
    limit = 30
    response = client.get(
        path='/api/foodproducts/',
        content_type='application/json',
        data={'limit': limit}
    )
    data = response.json()
    assert len(data['items']) == limit