from django.core.management import BaseCommand

from myfood.openAI import custom_open_ai_client


class Command(BaseCommand):
    def handle(self, *args, **options):
        response = custom_open_ai_client.billing_usage()
        print(response)