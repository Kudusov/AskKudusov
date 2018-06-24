from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.contrib import auth
from ask.models import Tag
from django.db.models import Q
from ask.forms import *
from ask.models import *
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
            # form.save()
            # return HttpResponseRedirect('/')
            return HttpResponseRedirect(form.save().get_url())
    else:
        form = PollForm()

    kwargs['form'] = form
    return render(request, 'ask.html', kwargs)


@base_decorator
@login_required(redirect_field_name='/login')
def single_chat(request, pers_id, **kwargs):
    recipient = User.objects.get(id=pers_id)
    if request.method == 'POST':
        form = PersonameMessageForm(request.user, recipient, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = PersonameMessageForm()

    kwargs['form'] = form
    sender = Profile.objects.get(user=request.user)
    recipient = Profile.objects.get(user=recipient)

    conversation = Conversation.objects.filter(sender=sender, recipient=recipient)
    if conversation.count() == 0:
        conversation = Conversation.objects.filter(sender=recipient, recipient=sender)

    messages = PersonalMessages.objects.filter(conversation=conversation).order_by('created_time')
    kwargs['messages'] = messages
    kwargs['recipient'] = recipient
    
    return render(request, 'chat.html', kwargs)


@base_decorator
def index(request, *args, **kwargs):
    print(request.META.get('HTTP_REFERER'))
    # questions = Question.objects.get_new()
    questions = UniversalQuestion.objects.get_new()
    for quest in questions:
        quest.text = quest.text.split('\n')

    return pagination(request=request, html_page='index.html', objects=questions, object_name='questions', objects_count=5, *args, **kwargs)


@base_decorator
def hot(request, *args, **kwargs):
    questions = UniversalQuestion.objects.get_hot_question()
    kwargs['header'] = "Hot Asks"
    return pagination(request, 'hot.html', questions, 'questions', 5, *args, **kwargs)


@base_decorator
def tag_python(request, tag_name, *args, **kwargs):
    questions = UniversalQuestion.objects.get_with_tag(tag_name)
    for quest in questions:
        quest.text = quest.text.split('\n')
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
    quest = UniversalQuestion.objects.get(id=question_id)
    quest.text = quest.text.split('\n')
    kwargs['question'] = quest
    answers = UniversalQuestion.objects.get_hot_answer(question=quest)
    return pagination(request, 'single_question.html', answers, 'answers', 5, **kwargs)


@base_decorator
def single_poll(request, answer_poll_id, **kwargs):

    if request.method == 'POST':
        poll_id = int(request.GET['poll_id'])
        print(poll_id)
        form = SimplePollResultForm(request.user, answer_poll_id, poll_id, request.POST)

        if form.is_valid():
            return HttpResponseRedirect(form.save().get_url())

    else:
        answer = UniversalQuestion.objects.get(id=answer_poll_id)
        polls = Poll.objects.filter(answer_poll=answer).order_by('id')
        forms = list()
        choices = list()
        for poll in polls:

            choice = list()
            poll_vars = PollVariant.objects.filter(poll=poll).order_by('id')
            for poll_var in poll_vars:
                # choice.append(AnswerPollVote.objects.filter(poll_varint=poll_var).count())
                poll_var_votes = AnswerPollVote.objects.filter(poll_varint=poll_var).count()
                all_votes = AnswerPollVote.objects.filter(poll=poll).count()
                if all_votes != 0:
                    all_votes = round(poll_var_votes / all_votes * 100, 2)

                choice.append([poll_var_votes, all_votes])
            choices.append(choice)
            forms.append(SimplePollResultForm(user=request.user, answer_poll_id=answer_poll_id, poll_id=poll.id))
        list_votes = [i*3 for i in range(3)]
        print(choices)
        kwargs['poll'] = answer
        kwargs['list_votes'] = choices
        kwargs['forms'] = forms
    return render(request, 'single_poll.html', kwargs)


@base_decorator
def poll_results(request, poll_id, **kwargs):
    # answer_poll = AnswerPoll.objects.get(id = poll_id)
    # polls = Poll.objects.filter(answer_poll=answer_poll)
    # poll_vars = list()
    # result = list()
    # for poll in polls:
    #     poll_var = PollVariant.objects.filter(poll=poll)
    #     poll_vars.append(poll_var)
    #     vote_nums = list()
    #     for p in poll_var:
    #         vote_nums.append(AnswerPollVote.objects.filter(poll=poll, poll_varint=p).count())
    #         print(AnswerPollVote.objects.filter(poll=poll, poll_varint=p).count())
    #     result.append(vote_nums)
    # print('result =', result)
    # zipped_poll_vars = list()
    # for i in range(len(poll_vars)):
    #     zipped_poll_vars.append(zip(poll_vars[i], result[i]))
    #
    # my_list = zip(polls, zipped_poll_vars)
    # kwargs['answer_poll'] = answer_poll
    # kwargs['polls'] = polls
    # kwargs['poll_vars'] = poll_vars
    # kwargs['my_list'] = my_list
    # return render(request, 'test_poll.html', kwargs)
    return render(request, 'poll_result.html', kwargs)


@login_required
def votes_view(request):
    type = request.GET['type']
    obj = request.GET['obj']
    id = request.GET['id']
    if obj == 'question':
        UniversalQuestionLike.objects.add_or_update_with_id(user=request.user, question_id=id, type=type)

    elif obj == 'answer':
        UniversalQuestionLike.objects.add_or_update_with_id(user=request.user, question_id=id, type=type)
        # AnswerLike.objects.add_or_update_with_id(user=request.user, answer_id=id, type=type)
    else:
        pass

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@base_decorator
def profile_view(request, user_id, **kwargs):

    profile_user = Profile.objects.get(user=User.objects.get(id=user_id))
    kwargs['profile_user'] = profile_user
    if request.user.is_authenticated:
        auth_user = Profile.objects.get(user=request.user)
        kwargs['is_auth_profile'] = profile_user == auth_user
    else:
        kwargs['is_auth_profile'] = False

    kwargs['answers'] = UniversalQuestion.objects.filter(author=profile_user, type='A').count()
    kwargs['questions'] = UniversalQuestion.objects.filter(author=profile_user, type='Q').count()
    kwargs['polls'] = UniversalQuestion.objects.filter(author=profile_user, type='P').count()
    kwargs['followers'] = 0
    kwargs['followings'] = 0

    return render(request, 'test_user_profile2.html', kwargs)


@base_decorator
@login_required(redirect_field_name='/login')
def main_profile_view(request, **kwargs):

    profile_user = Profile.objects.get(user=request.user)
    kwargs['profile_user'] = profile_user
    if request.user.is_authenticated:
        auth_user = Profile.objects.get(user=request.user)
        kwargs['is_auth_profile'] = profile_user == auth_user
    else:
        kwargs['is_auth_profile'] = False

    kwargs['answers'] = UniversalQuestion.objects.filter(author=profile_user, type='A').count()
    kwargs['questions'] = UniversalQuestion.objects.filter(author=profile_user, type='Q').count()
    kwargs['polls'] = UniversalQuestion.objects.filter(author=profile_user, type='P').count()
    kwargs['followers'] = 0
    kwargs['followings'] = 0

    return render(request, 'test_user_profile2.html', kwargs)

@base_decorator
def msg_list_view(request, user_id, **kwargs):
    profile_user = Profile.objects.get(user=User.objects.get(id=user_id))
    if profile_user.user != request.user:
        return HttpResponseRedirect('/')

    kwargs['profile_user'] = profile_user
    if request.user.is_authenticated:
        auth_user = Profile.objects.get(user=request.user)
        kwargs['is_auth_profile'] = profile_user == auth_user
    else:
        kwargs['is_auth_profile'] = False

    kwargs['answers'] = UniversalQuestion.objects.filter(author=profile_user, type='A').count()
    kwargs['questions'] = UniversalQuestion.objects.filter(author=profile_user, type='Q').count()
    kwargs['polls'] = UniversalQuestion.objects.filter(author=profile_user, type='P').count()
    kwargs['followers'] = 0
    kwargs['followings'] = 0

    convers = Conversation.objects.filter(Q(sender=profile_user) | Q(recipient=profile_user))

    messages = []
    for conv in convers:
        print(conv.id)
        msg = PersonalMessages.objects.filter(conversation=conv).order_by('-created_time')
        if msg.count() != 0:
            messages.append(msg[0])
    messages.sort(key=lambda x: x.created_time)
    # messages.sort(key=lambda message: message.created_time)
    for message in messages:
        print(message.conversation.id)
    kwargs['messages'] = messages
    # dialogs = PersonalMessages.objects.filter(Q(conversation__sender=request.user) | Q(conversation__recipient=))

    return render(request, 'message_list.html', kwargs)

# @base_decorator
# def single_chat(request, pers_id, **kwargs):
#     return render(request, 'chat.html', kwargs)

class AboutView(TemplateView):
    pass

# Create your views here.
