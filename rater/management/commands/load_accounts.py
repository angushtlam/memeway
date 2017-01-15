from django.core.management.base import BaseCommand, CommandError
from memeway import random_generator
from rater.models import Meme, MemeImage, User, ChatRoom
import random


class Command(BaseCommand):
    help = 'Loads all the memes from the interwebs'

    def add_arguments(self, parser):
        parser.add_argument('accounts', type=int)

    def handle(self, *args, **options):

        names = ["diane", "jack", "jill", "bridget", "collin", "julia", "rainbowgurl", "xoxgirlxox"]

        for user in User.objects.all():
            if user.username not in ["dan", "angus"]:
                user.delete()

        for chat in ChatRoom.objects.all():
            chat.delete()

        accounts = options['accounts']

        users = []

        for num in range(0, accounts):

            if num == 0:
                username = "memecat"
            else:
                username = random.choice(names) + str(num)

            user = User.objects.create_user(username, password=random_generator())

            user.save()

            users.append(user)

            random_images = random.sample(list(MemeImage.objects.all()), 9)

            for image in random_images:
                image.users_who_liked.add(user)
                image.save()

        # Make connections
        for user in users:
            random_users = random.sample(list(User.objects.all()), int(accounts/2))

            for rand_user in random_users:
                if user != rand_user:
                    user.liked.add(rand_user)
                    user.save()

                    if user in rand_user.liked.all():
                        user.matches.add(rand_user)
                        rand_user.matches.add(user)
                        rand_user.save()
                        user.save()
                        chat = ChatRoom.objects.create()
                        chat.users.add(rand_user)
                        chat.users.add(user)
                        chat.save()
