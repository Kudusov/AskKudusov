from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from ask.models import Profile
from faker import Faker


class Command(BaseCommand):
    help = 'Add Users'

    def add_arguments(self, parser):
        parser.add_argument('--number', action='store', dest='number', default=5, help='number of users')

    def handle(self, *args, **options):
        fake = Faker('en_US')
        count = int(options['number'])
        added = 0

        for i in range(count):
            profile = fake.simple_profile()
            user = User.objects.create_user(profile['username'], profile['mail'], make_password('test'))
            user.first_name = fake.first_name()
            user.last_name = fake.last_name()
            user.is_active = True
            user.is_superuser = False
            user.save()

            user_profile = Profile()
            user_profile.user = user
            user_profile.save()

            added += 1

        print(added, " Users is added")
