from django.core.management.base import BaseCommand, CommandError
import bs4
import urllib.request

from rater.models import Meme, MemeImage

class Command(BaseCommand):
    help = 'Delete any memes that have zero images'

    def handle(self, *args, **options):
        for meme in Meme.objects.all():
            if len(meme.images.all()) == 0:
                self.stdout.write(self.style.SUCCESS('Successfully deleted %s.' % meme.title))
                meme.delete()

        print(len(Meme.objects.all()))

        self.stdout.write(self.style.SUCCESS('Successfully deleted some of the memes.'))