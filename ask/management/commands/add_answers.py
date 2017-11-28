from django.core.management.base import BaseCommand
from ask.models import Question
from ask.models import Answer
from ask.models import Profile
from faker import Faker
from random import choice, randint


class Command(BaseCommand):
    help = 'Add Questions'

    def add_arguments(self, parser):
        parser.add_argument('--number', action='store', dest='number', default=7, help='number of questions')

    def handle(self, *args, **options):
        fake = Faker('en_US')
        users = Profile.objects.all()[1:]
        questions = Question.objects.all()
        added = 0

        for question in questions:
            answer = Answer()
            answer.text = fake.text(randint(200, 400))
            answer.question = question
            answer.author = choice(users)
            answer.save()
            added += 1

        print(added, " Answer is added")
