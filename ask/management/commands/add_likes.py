from django.core.management.base import BaseCommand
from ask.models import UniversalQuestion, UniversalQuestionLike
from ask.models import Profile
from random import choice


class Command(BaseCommand):
    help = 'Add Likes'

    def add_arguments(self, parser):
        parser.add_argument('--number-questions', action='store', dest='number-questions', default=5,
                            help='number of likes for question')
        parser.add_argument('--number-answers', action='store', dest='number-answers', default=5,
                            help='number of likes for answer')

    def handle(self, *args, **options):
        count_questions = int(options['number-questions'])
        # count_answers = int(options['number-answers'])
        users = Profile.objects.all()[1:]
        questions = UniversalQuestion.objects.all()
        added = 0

        for question in questions:
            for i in range(count_questions):
                UniversalQuestionLike.objects.add_or_update(author=choice(users), question=question, value=choice([1, -1]))
                added += 1

        print(added, " Likes for question is added")

        # added = 0
        # answers = Uni.objects.all()
        #
        # for answer in answers:
        #     for i in range(count_answers):
        #         UniversalQuestionLikes.objects.add_or_update(author=choice(users), answer=answer, value=choice([1, -1]))
        #         added += 1
        #
        # print(added, " Likes for answers is added")
