from django.core.management.base import BaseCommand

from myfood import logger
from myfood.factories import FoodProductFactory

class Command(BaseCommand):
    help = 'Populate FoodProduct table with dummy data'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10000, help='Number of food products to create')

    def handle(self, *args, **options):
        count = options['count']
        FoodProductFactory.create_batch(count)
        logger.info(f'Successfully created {count} food products.')
