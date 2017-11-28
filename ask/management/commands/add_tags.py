from django.core.management.base import BaseCommand
from ask.models import Tag
import random


class Command(BaseCommand):
    help = 'Add Tags'

    def add_arguments(self, parser):
        parser.add_argument('--number', action='store', dest='number', default=5, help='number of tags')

    def handle(self, *args, **options):
        def get_rand_color():
            return random.choice(['red', 'orange', 'blue', 'green', 'cyan', 'violet', 'teal', 'maroon',
                                  'indigo', 'peru'])

        tags = ['Technopark', 'C++', 'Java', 'Python', 'Perl', 'Django', 'Apple', 'Android',
                'Haskell', 'CSS', 'HTML', 'Bootstrap', 'Twitter', 'Vkontakte', 'Facebook', 'IOS',
                'Windows']

        added = 0

        for tag in tags:
            if len(Tag.objects.filter(title=tag)) == 0:
                t = Tag()
                t.title = tag
                t.color = get_rand_color()
                t.save()
                added += 1

        print(added, " Tags is added")
