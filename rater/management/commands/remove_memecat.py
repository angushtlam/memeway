from django.core.management.base import BaseCommand, CommandError
import bs4
import urllib.request

from rater.models import ChatRoom, User


class Command(BaseCommand):
    help = 'Delete any memes that have zero images'

    def handle(self, *args, **options):

        memecat = User.objects.filter(username="memecat").first()

        if not memecat:
            return

        for chat in ChatRoom.objects.all():
            if memecat in chat.users.all():
                chat.delete()

        memecat.delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted memecat.'))
