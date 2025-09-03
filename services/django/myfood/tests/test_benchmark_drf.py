from rest_framework.test import APIClient
import pytest
from myfood.factories import FoodProductFactory

@pytest.mark.benchmark(group='list-json-1000-in-50')
@pytest.mark.parametrize('default_url', ['/api/foodproducts/search/', '/api/foodproducts-orjson/search/', '/api/foodproducts-msgspec/search/'])
@pytest.mark.django_db
def test_base_benchmark(benchmark, default_url):
    batch = 1000
    limit = 50
    FoodProductFactory.create_batch(batch)
    client = APIClient()
    state = {'offset': 0}
    
    def do_request():
        url = f'{default_url}?limit={limit}&offset={state["offset"]}'
        resp = client.get(url)
        state['offset'] += limit
        _ = resp.content
        return resp.status_code

    benchmark.pedantic(
        do_request,
        iterations=1,
        rounds=int(batch/limit),
        warmup_rounds=0,
    )