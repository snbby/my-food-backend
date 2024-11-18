from django.core.management import BaseCommand
from faker import Faker

from myfood.models import ModelChat


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()
        fake_sentence = faker.sentence(nb_words=20)
        print(fake_sentence)
        chat = ModelChat(user_input=fake_sentence)
        chat.save()
        print(chat.model_answer)
