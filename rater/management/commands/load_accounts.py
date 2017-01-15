from django.core.management.base import BaseCommand, CommandError
from memeway import random_generator
from rater.models import Meme, MemeImage, User
import random


class Command(BaseCommand):
    help = 'Loads all the memes from the interwebs'

    def add_arguments(self, parser):
        parser.add_argument('accounts', type=int)

    def handle(self, *args, **options):

        for user in User.objects.all():
            if user.username not in ["dan", "angus"]:
                user.delete()

        accounts = options['accounts']

        for num in range(0, accounts):

            username = random_generator()

            user = User.objects.create_user(username, random_generator(), "Example User", str(num))

            user.save()

            random_images = random.sample(list(MemeImage.objects.all()), 6)

            for image in random_images:
                image.users_who_liked.add(user)
                image.save()
