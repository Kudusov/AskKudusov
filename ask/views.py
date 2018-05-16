from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.contrib import auth
from ask.models import Tag, Question
from ask.forms import *
from django.contrib.auth.decorators import login_required
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
        # name = faker.name()
        # kwargs['is_autentificated'] = get_rand_bool()
        # kwargs['name'] = name
        kwargs['best_members'] = best_members
        kwargs['popular_tags'] = popular_tags
        return func(request, *args, **kwargs)

    return decorator


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
    print(request.META.get('HTTP_REFERER'))
    if request.user.is_authenticated():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/')

    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return HttpResponseRedirect('/')

    else:
        form = LoginForm()

    kwargs['form'] = form
    return render(request, 'login.html', kwargs)


def logout(request, **kwargs):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/')


@base_decorator
def signup(request, *args, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'), '/')

    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            auth.login(request, user)

            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/login')
    else:
        form = SignupForm()

    kwargs['form'] = form
    return render(request, 'signup.html', kwargs)

    # return render(request, 'signup.html', {
    #     'form': form,
    #     'tags': kwargs['tags'],
    # })

    # return render(request, 'signup.html', kwargs)


@base_decorator
@login_required(redirect_field_name='/login')
def ask(request, *args, **kwargs):

    if request.method == 'POST':
        form = QuestionForm(request.user, request.POST)

        if form.is_valid():
            return HttpResponseRedirect(form.save().get_url())

    else:
        form = QuestionForm()
    print(request.META.get('HTTP_REFERER'))
    kwargs['form'] = form
    return render(request, 'ask.html', kwargs)


@base_decorator
@login_required(redirect_field_name='/login')
def poll(request, *args, **kwargs):
    if request.method == 'POST':
        form = PollForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            # return HttpResponseRedirect('/')
            return HttpResponseRedirect(form.save().get_url())

    else:
        form = PollForm()

    kwargs['form'] = form
    return render(request, 'ask.html', kwargs)


@base_decorator
def index(request, *args, **kwargs):
    print(request.META.get('HTTP_REFERER'))
    questions = Question.objects.get_new()
    for quest in questions:
        quest.text = quest.text.split('\n')

    return pagination(request=request, html_page='index.html', objects=questions, object_name='questions', objects_count=5, *args, **kwargs)


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
    print(request.META.get('HTTP_REFERER'))
    if request.method == 'POST':

        form = AnswerForm(request.user, question_id, request.POST)

        if form.is_valid():
            return HttpResponseRedirect(form.save().get_url())

    else:
        form = AnswerForm()

    kwargs['form'] = form
    quest = Question.objects.get(id=question_id)
    quest.text = quest.text.split('\n')
    kwargs['question'] = quest
    answers = quest.get_answers().all()
    return pagination(request, 'single_question.html', answers, 'answers', 5, **kwargs)


@base_decorator
def single_poll(request, answer_poll_id, **kwargs):
    if request.method == 'POST':
        form = PollResultsForm(request.user, answer_poll_id, request.POST)

        if form.is_valid():
            return HttpResponseRedirect(form.save().get_url())

    else:
        form = PollResultsForm(request.user, answer_poll_id)

    kwargs['form'] = form
    return render(request, 'single_poll.html', kwargs)


@base_decorator
def poll_results(request, poll_id, **kwargs):
    answer_poll = AnswerPoll.objects.get(id = poll_id)
    polls = Poll.objects.filter(answer_poll=answer_poll)
    poll_vars = list()
    result = list()
    for poll in polls:
        poll_var = PollVariant.objects.filter(poll=poll)
        poll_vars.append(poll_var)
        vote_nums = list()
        for p in poll_var:
            vote_nums.append(AnswerPollVote.objects.filter(poll=poll, poll_varint=p).count())
            print(AnswerPollVote.objects.filter(poll=poll, poll_varint=p).count())
        result.append(vote_nums)
    print('result =', result)
    zipped_poll_vars = list()
    for i in range(len(poll_vars)):
        zipped_poll_vars.append(zip(poll_vars[i], result[i]))

    my_list = zip(polls, zipped_poll_vars)
    kwargs['answer_poll'] = answer_poll
    kwargs['polls'] = polls
    kwargs['poll_vars'] = poll_vars
    kwargs['my_list'] = my_list
    # return render(request, 'test_poll.html', kwargs)
    return render(request, 'poll_result.html', kwargs)


@login_required
def votes_view(request):
    type = request.GET['type']
    obj = request.GET['obj']
    id = request.GET['id']
    if obj == 'question':
        QuestionLike.objects.add_or_update_with_id(user=request.user, question_id=id, type=type)

    elif obj == 'answer':
        AnswerLike.objects.add_or_update_with_id(user=request.user, answer_id=id, type=type)
    else:
        pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AboutView(TemplateView):
    pass

# Create your views here.
