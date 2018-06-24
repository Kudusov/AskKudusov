# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='uploads')


class TagManager(models.Manager):
    def add_question_count(self):
        return self.annotate(questions_count=Count('universalquestion'))

    def order_by_question_count(self):
        return self.add_question_count().order_by('-questions_count')

    def get_by_title(self, title):
        return self.get(title=title)

    def get_popular(self):
        # questions_count = Count('question')
        return self.order_by_question_count().all()[:10]


class Tag(models.Model):
    title = models.CharField(max_length=20)
    color = models.CharField(max_length=20, default='blue')
    objects = TagManager()

    def get_url(self):
        return '/tag/{tag_title}'.format(tag_title=self.title)


# class QuestionManager(models.Manager):
#     def get_new(self):
#         return self.order_by('-created_date')
#
#     def get_hot(self):
#         return self.order_by('-likes')
#
#     def get_with_tag(self, tag):
#         return self.filter(tags__title=tag)


# class Question(models.Model):
#     title = models.CharField(max_length=30)
#     text = models.TextField()
#     author = models.ForeignKey(Profile)
#     created_date = models.DateTimeField(default=timezone.now)
#     tags = models.ManyToManyField(Tag)
#     likes = models.IntegerField(default=0)
#
#     objects = QuestionManager()
#
#     class Meta:
#         db_table = 'question'
#         ordering = ['-created_date']
#
#     def get_answers(self):
#         return Answer.objects.filter(question_id=self.id)
#
#     def get_url(self):
#         return '/question/{question_id}'.format(question_id=self.id)


class UniversalQuestionManager(models.Manager):
    def get_new(self):
        return self.filter(Q(type='Q') | Q(type='P')).order_by('-created_date')

    def get_new_question(self):
        return self.filter(type='Q').order_by('-created_date')

    def get_new_answer(self, question):
        return self.filter(type='A', parent=question).order_by('-created_date')

    def get_new_polls(self):
        return self.filter(type='P').order_by('-created_date')

    def get_hot(self):
        return self.filter(Q(type='Q') | Q(type='P')).order_by('-likes')

    def get_hot_question(self):
        return self.filter(type='Q').order_by('-likes')

    def get_hot_answer(self, question):
        return self.filter(type='A', parent=question).order_by('-likes')

    def get_hot_polls(self):
        return self.filter(type='P').order_by('-likes')

    def get_with_tag(self, tag):
        return self.filter(tags__title=tag)


class UniversalQuestion(models.Model):
    TYPES = (
        ('Q', 'Question'),
        ('A', 'Answer'),
        ('P', 'QuestionPoll'),
    )
    title = models.CharField(max_length=30)
    text = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag)
    likes = models.IntegerField(default=0)
    parent = models.ForeignKey('self', null=True)
    type = models.CharField(max_length=1, choices=TYPES)
    objects = UniversalQuestionManager()

    class Meta:
        ordering = ['-created_date']

    def get_answers(self):
        return UniversalQuestion.objects.filter(parent=self)

    def get_url(self):

        if self.type == 'Q':
            return '/question/{question_id}'.format(question_id=self.id)
        elif self.type == 'A':
            return '/question/{question_id}'.format(question_id=self.parent.id)
        else:
            return '/poll/{poll_id}'.format(poll_id=self.id)


# class QuestionLikeManager(models.Manager):
#     def get_with_sum(self, question):
#         return self.filter(question=question).aggregate(sum=Sum('value'))['sum']
#
#     def add_or_update(self, author, question, value):
#         obj, new = self.update_or_create(author=author, question=question, defaults={'value': value})
#
#         question.likes = self.get_with_sum(question)
#         question.save()
#
#         return new
#
#     def add_or_update_with_id(self, user, question_id, type):
#         if type == 'dislike':
#             value = -1
#         else:
#             value = 1
#         author = Profile.objects.get(user=user)
#         question = Question.objects.get(id=question_id)
#         self.add_or_update(author=author, question=question, value=value)


# class QuestionLike(models.Model):
#     question = models.ForeignKey(Question)
#     author = models.ForeignKey(Profile)
#     value = models.SmallIntegerField(default=1)
#
#     objects = QuestionLikeManager()


class UniversalQuestionLikeManager(models.Manager):
    def get_with_sum(self, question):
        return self.filter(question=question).aggregate(sum=Sum('value'))['sum']

    def add_or_update(self, author, question, value):
        obj, new = self.update_or_create(author=author, question=question, defaults={'value': value})

        question.likes = self.get_with_sum(question)
        question.save()

        return new

    def add_or_update_with_id(self, user, question_id, type):
        if type == 'dislike':
            value = -1
        else:
            value = 1
        author = Profile.objects.get(user=user)
        question = UniversalQuestion.objects.get(id=question_id)
        self.add_or_update(author=author, question=question, value=value)


class UniversalQuestionLike(models.Model):
    question = models.ForeignKey(UniversalQuestion)
    author = models.ForeignKey(Profile)
    value = models.SmallIntegerField(default=1)
    objects = UniversalQuestionLikeManager()


# class Answer(models.Model):
#     text = models.TextField()
#     question = models.ForeignKey(Question)
#     author = models.ForeignKey(Profile)
#     created_date = models.DateTimeField(default=timezone.now)
#     correct = models.BooleanField(default=False)
#     likes = models.IntegerField(default=0)
#
#     class Meta:
#         db_table = 'answer'
#
#     def get_url(self):
#         return self.question.get_url()


# class AnswerLikeManager(models.Manager):
#     def get_with_sum(self, answer):
#         return self.filter(answer=answer).aggregate(sum=Sum('value'))['sum']
#
#     def add_or_update(self, author, answer, value):
#         obj, new = self.update_or_create(author=author, answer=answer, defaults={'value': value})
#
#         answer.likes = self.get_with_sum(answer)
#         answer.save()
#
#         return new
#
#     def add_or_update_with_id(self, user, answer_id, type):
#         if type == 'dislike':
#             value = -1
#         else:
#             value = 1
#         author = Profile.objects.get(user=user)
#         answer = Answer.objects.get(id=answer_id)
#         self.add_or_update(author=author, answer=answer, value=value)


# class AnswerLike(models.Model):
#     answer = models.ForeignKey(Answer)
#     author = models.ForeignKey(Profile)
#     value = models.SmallIntegerField(default=1)
#
#     objects = AnswerLikeManager()


# class AnswerPoll(models.Model):
#     title = models.CharField(max_length=30)
#     text = models.TextField()
#     author = models.ForeignKey(Profile)
#     created_date = models.DateTimeField(default=timezone.now)
#
#     def get_url(self):
#         return '/poll/{poll_id}'.format(poll_id=self.id)


class Poll(models.Model):
    answer_poll = models.ForeignKey(UniversalQuestion)
    answer = models.CharField(max_length=30)


class PollVariant(models.Model):
    poll = models.ForeignKey(Poll)
    text = models.CharField(max_length=30)


class AnswerPollVoteManager(models.Manager):
    def add_or_update(self, author, answer_poll, poll, poll_variant):
        obj, new = self.update_or_create(author=author, answer_poll=answer_poll, poll=poll, defaults={'poll_varint': poll_variant})
        return new


class AnswerPollVote(models.Model):
    author = models.ForeignKey(Profile)
    answer_poll = models.ForeignKey(UniversalQuestion)
    poll = models.ForeignKey(Poll)
    poll_varint = models.ForeignKey(PollVariant)
    objects = AnswerPollVoteManager()


class Conversation(models.Model):
    sender = models.ForeignKey(Profile, related_name='sender')
    recipient = models.ForeignKey(Profile, related_name='recipient')
    last_msg = models.DateTimeField(default=timezone.now)


class PersonalMessages(models.Model):
    conversation = models.ForeignKey(Conversation)
    text = models.TextField()
    author = models.ForeignKey(Profile)
    created_time = models.DateTimeField(default=timezone.now)

# Create your models here.
