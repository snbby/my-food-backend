from django.core.management import BaseCommand
from faker import Faker

from myfood.models import ModelOpenAIImageGeneration


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()
        image = ModelOpenAIImageGeneration(
            prompt=faker.sentence(nb_words=10), 
            image_resolution=ModelOpenAIImageGeneration.OpenAIImageResolution.s1024x1024, 
            use_dalle3=True
        )
        image.save()
