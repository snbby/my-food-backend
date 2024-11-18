from django.core.management import BaseCommand
from django.conf import settings

from myfood.s3 import s3_client


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(f'{settings.BASE_DIR}/artifacts/ava.png', 'rb') as f:
            image_link = s3_client.upload_fileobj(f, bucket='me-proj', path='ava.png')
        
        print(image_link)
