from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ask.models import Tag, Question
from faker import Faker
import random


class _Question:
    def __init__(self):
        faker = Faker()
        self.likes = random.randint(-99, 99)
        self.answers = random.randint(0, 99)
        self.tags = [get_rand_tag() for _ in range(random.randint(1, 3))]
        self.title = faker.sentence(5)
        self.text = faker.text(300)


def get_rand_bool():
    return random.choice([True, False])


def get_rand_tag():
    return random.choice(['Technopark', 'C++', 'Java', 'Python', 'Perl', 'Django', 'Apple', 'Android',
                          'Haskell', 'CSS', 'HTML', 'Bootstrap', 'Twitter', 'Vkontakte', 'Facebook'])


def get_rand_color():
    return random.choice(['red', 'orange', 'blue', 'green', 'cyan', 'violet', 'teal', 'maroon',
                          'indigo', 'peru'])


def foo(request):
    return render(request, 'hello.html', {
        'title': 'Hello Title',
        'text': 'Some Text',
    })


# context_processors || inclusion tags || django custom tags
def base_decorator(func):
    def decorator(request, *args, **kwargs):
        faker = Faker()
        popular_tags = Tag.objects.get_popular()
        best_members = [faker.name() for _ in range(5)]
        # is_autentificated = get_rand_bool()
        name = faker.name()
        kwargs['is_autentificated'] = get_rand_bool()
        kwargs['name'] = name
        kwargs['best_members'] = best_members
        kwargs['popular_tags'] = popular_tags
        return func(request, *args, **kwargs)

    return decorator


# def tags_decorator(func):

# 	def decorator(request, *args, **kwargs):
# 		tags = [Tag() for _ in range(8)]

# 		return func(request, tags=tags, *args, **kwargs)

# 	return decorator


def pagination(request, html_page, objects, object_name, objects_count, *args, **kwargs):
    paginator = Paginator(objects, objects_count)
    page = request.GET.get('page')

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    kwargs[object_name] = objects
    kwargs['pagination_list'] = objects

    return render(request, html_page, kwargs)


# def login(request):
# 	faker = Faker()

# 	return render(request, 'login.html' , {
# 		'is_autentificated' : get_rand_bool(),
# 		'name': faker.name(),
# 		'email_correct': get_rand_bool(),
# 		'pwd_correct': get_rand_bool()
# 	})


@base_decorator
def login(request, *args, **kwargs):
    kwargs['email_correct'] = get_rand_bool()
    kwargs['pwd_correct'] = get_rand_bool()
    return render(request, 'login.html', kwargs)


@base_decorator
def signup(request, *args, **kwargs):
    kwargs['login_correct'] = get_rand_bool()
    kwargs['email_correct'] = get_rand_bool()
    kwargs['nickname_correct'] = get_rand_bool()
    kwargs['pwd_correct'] = get_rand_bool()
    kwargs['conf_pwd_correct'] = get_rand_bool()

    return render(request, 'signup.html', kwargs)


@base_decorator
def ask(request, *args, **kwargs):
    return render(request, 'ask.html', kwargs)


@base_decorator
def index(request, *args, **kwargs):
    questions = Question.objects.get_new()
    return pagination(request, 'index.html', questions, 'questions', 5, *args, **kwargs)


@base_decorator
def hot(request, *args, **kwargs):
    questions = Question.objects.get_hot()
    kwargs['header'] = "Hot Asks"
    return pagination(request, 'hot.html', questions, 'questions', 5, *args, **kwargs)


@base_decorator
def tag_python(request, tag_name, *args, **kwargs):
    questions = Question.objects.get_with_tag(tag_name)
    kwargs['header'] = "Tag: " + tag_name
    return pagination(request, 'hot.html', questions, 'questions', 5, *args, **kwargs)


@base_decorator
def single_question(request, question_id, **kwargs):
    kwargs['question'] = Question.objects.get(id=question_id)
    answers = kwargs['question'].get_answers()
    return pagination(request, 'single_question.html', answers, 'answers', 5, **kwargs)


class AboutView(TemplateView):
    pass

# Create your views here.
