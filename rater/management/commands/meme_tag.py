from django.core.management.base import BaseCommand, CommandError
from rater.models import Meme


class Command(BaseCommand):
    help = 'Loads all the memes from the interwebs'

    def handle(self, *args, **options):

        for meme in Meme.objects.all():
            meme.build_tags()

        self.stdout.write(self.style.SUCCESS('Successfully tagged all the memes.'))