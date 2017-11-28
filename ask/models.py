# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='uploads')


class TagManager(models.Manager):
    def add_question_count(self):
        return self.annotate(questions_count=Count('question'))

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


class QuestionManager(models.Manager):
    def get_new(self):
        return self.order_by('-created_date')

    def get_hot(self):
        return self.order_by('-likes')

    def get_with_tag(self, tag):
        return self.filter(tags__title=tag)


class Question(models.Model):
    title = models.CharField(max_length=30)
    text = models.TextField()
    author = models.ForeignKey(Profile)
    created_date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag)
    likes = models.IntegerField(default=0)

    objects = QuestionManager()

    class Meta:
        db_table = 'question'
        ordering = ['-created_date']

    def get_answers(self):
        return Answer.objects.filter(question_id=self.id)

    def get_url(self):
        return '/question/{question_id}'.format(question_id=self.id)


class QuestionLikeManager(models.Manager):
    def get_with_sum(self, question):
        return self.filter(question=question).aggregate(sum=Sum('value'))['sum']

    def add_or_update(self, author, question, value):
        obj, new = self.update_or_create(author=author, question=question, defaults={'value': value})

        question.likes = self.get_with_sum(question)
        question.save()

        return new


class QuestionLike(models.Model):
    question = models.ForeignKey(Question)
    author = models.ForeignKey(Profile)
    value = models.SmallIntegerField(default=1)

    objects = QuestionLikeManager()


class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question)
    author = models.ForeignKey(Profile)
    created_date = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)

    class Meta:
        db_table = 'answer'

    def get_url(self):
        return self.question.get_url()


class AnswerLikeManager(models.Manager):
    def get_with_sum(self, answer):
        return self.filter(answer=answer).aggregate(sum=Sum('value'))['sum']

    def add_or_update(self, author, answer, value):
        obj, new = self.update_or_create(author=author, answer=answer, defaults={'value': value})

        answer.likes = self.get_with_sum(answer)
        answer.save()

        return new


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer)
    author = models.ForeignKey(Profile)
    value = models.SmallIntegerField(default=1)

    objects = AnswerLikeManager()

# Create your models here.
