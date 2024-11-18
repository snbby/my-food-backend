from django.core.management import BaseCommand

from myfood.openAI import custom_open_ai_client

class Command(BaseCommand):
    def handle(self, *args, **options):
        input = 'Hello, this is AI created voice by Max'
        response = custom_open_ai_client.create_audio(prompt=input)
        with open('my_track.mp3', 'wb') as f:
            f.write(response.content)
