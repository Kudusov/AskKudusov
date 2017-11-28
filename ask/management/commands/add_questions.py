from django.core.management.base import BaseCommand
from ask.models import Question, Tag
from ask.models import Profile
from faker import Faker
from random import choice, randint


class Command(BaseCommand):
    help = 'Add Questions'

    def add_arguments(self, parser):
        parser.add_argument('--number', action='store', dest='number', default=5, help='number of questions')

    def handle(self, *args, **options):
        fake = Faker('en_US')
        count = int(options['number'])
        users = Profile.objects.all()[1:]
        added = 0
        tags = Tag.objects.all()

        for i in range(count):
            question = Question()
            question.title = fake.sentence(nb_words=3)
            question.text = fake.text(randint(300, 600))
            question.author = choice(users)
            question.date = fake.date()
            question.save()
            added += 1

        for quest in Question.objects.all():
            if len(quest.tags.all()) < 2:
                for i in range(2 - len(quest.tags.all())):
                    t = choice(tags)
                    if t not in quest.tags.all():
                        quest.tags.add(choice(tags))

        print(added, " Questions is added")
