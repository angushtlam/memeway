from django.core.management.base import BaseCommand, CommandError
import bs4
import urllib.request
from time import sleep

from rater.models import Meme, MemeImage


class Command(BaseCommand):
    help = 'Loads all the memes from the interwebs'

    def add_arguments(self, parser):
        parser.add_argument('pages', type=int)

        parser.add_argument(
            '--start',
            action='store_true',
            dest='delete',
            default=False,
            help='Start page',
        )

    def handle(self, *args, **options):

        BLOCKED = ["shantae", "zettai"]

        pages = options['pages']

        # Start fresh
        for meme in Meme.objects.all():
            meme.delete()

        # Iterate through all the pages
        for page in range(1, pages+1):

            print("***** PAGE %s *****" % page)

            url = "http://knowyourmeme.com/memes/page/%s" % page
            r = urllib.request.urlopen(url).read()

            # The bs4 soup that has the page of memes
            meme_list_soup = bs4.BeautifulSoup(r, "html.parser")

            if meme_list_soup is None:
                break

            meme_cells = meme_list_soup.find("table", class_="entry_list").find_all("td")

            for meme in meme_cells:

                anchor = meme.find("h2").find("a")

                name = anchor.contents[0]

                link = anchor["href"]

                if Meme.objects.filter(title=name).first() or name.lower() in BLOCKED:
                    continue

                # Follow link to meme
                url = "http://knowyourmeme.com%s" % link
                meme_page = bs4.BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser").find("section", class_="bodycopy")

                if meme_page is None:
                    break

                images = meme_page.find_all("img")

                # Create the actual meme
                meme_obj = Meme.objects.create(title=name)
                meme_obj.save()
                meme_obj.build_tags()

                for image in images:
                    a = image.get("data-src", "")

                    if len(a) > 5:
                        m_image = MemeImage.objects.create(meme=meme_obj, url=a)
                        m_image.save()

                print("Successfully created %s meme with %s image(s)." % (meme_obj.title, len(meme_obj.images.all() )))

            print("")

            sleep(0.1)

        self.stdout.write(self.style.SUCCESS('Successfully got all the memes.'))