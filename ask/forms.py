from datetime import datetime
from django import forms
from django.contrib.auth import authenticate
from .models import *
from django.contrib.auth.models import User

import os


class PollResultsForm(forms.Form):
    def __init__(self, user=None, poll_id=None, *args, **kwargs):
        self.user = user
        self.poll_id = poll_id
        answer = AnswerPoll.objects.get(id=poll_id)
        polls = Poll.objects.filter(answer_poll=answer).order_by('id')

        super(PollResultsForm, self).__init__(*args, **kwargs)
        for i in range(len(polls)):
            choice = list()
            poll_vars = PollVariant.objects.filter(poll=polls[i]).order_by('id')

            for j in range(len(poll_vars)):
                choice.append([str(j), poll_vars[j].text])

            self.fields[str(i)] = forms.ChoiceField(
                widget=forms.RadioSelect(), choices=choice, label=polls[i].answer
    )


class LoginForm(forms.Form):
    # status = forms.ChoiceField(
    #     widget=forms.RadioSelect(), choices=[['a', 'Radio 1'], ['b', 'Radio 2']]
    # )
    # def __init__(self, *args, **kwargs):
    #     super(LoginForm, self).__init__(*args, **kwargs)
    #     for i in range(5):
    #         self.fields[str(i)] = forms.ChoiceField(
    #             widget=forms.RadioSelect(), choices=[['a', 'Radio 1'], ['b', 'Radio 2']]
    # )

    statuses = list()
    statuses.append(forms.ChoiceField(
        widget=forms.RadioSelect(), choices=[['a', 'Radio 1'], ['b', 'Radio 2']]
    ))
    statuses.append(forms.ChoiceField(
        widget=forms.RadioSelect(), choices=[['a', 'Radio 1'], ['b', 'Radio 2']]
    ))

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'style': 'max-height: 35px', 'placeholder': 'Enter your login...', }
        ),
        max_length=20,
        label='Login',
    )
    # type = "password"
    #
    # class ="form-control" id="pwd"
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'type': 'password', 'class': 'form-control', 'style': 'max-height: 35px', 'placeholder': 'Enter your password...', }
        ),
        min_length=8,
        label='Password',
    )

    def clean(self):
        user = authenticate(username=self.cleaned_data['username'],
                            password=self.cleaned_data['password']
                            )
        # print('\n\nstatus0 = ', self.cleaned_data['0'], '\n\n')
        # print('\n\nstatus1 = ', self.cleaned_data['1'], '\n\n')
        # print('\n\nstatus2 = ', self.cleaned_data['2'], '\n\n')

        if user is not None:

            if user.is_active:
                self.cleaned_data['user'] = user
            else:
                raise forms.ValidationError('This user is\'t active!!!')
        else:
            raise forms.ValidationError('Invalid login or password!!!')


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter login...'}
        ),
        max_length=20,
        label='Login',
    )

    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your first name...'}
        ),
        max_length=20,
        label='First name',
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your last name login...'}
        ),
        max_length=20,
        label='Last name',
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter e-mail...'}
        ),
        max_length=30,
        label='E-mail',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter password...'}
        ),
        min_length=8,
        label='Password',
    )

    repeat_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Renter password...'}
        ),
        min_length=8,
        label='Repeat password',
    )

    # avatar = forms.ImageField(
    #     required=False,
    #     widget=forms.FileInput(
    #         attrs={'class': 'form-control', }
    #     ),
    #     label='Avatar'
    # )

    def clean_username(self):
        try:
            user = User.objects.get(username=self.cleaned_data['username'])
            raise forms.ValidationError('User already exists!!!')
        except User.DoesNotExist:
            return self.cleaned_data['username']

    def clean_repeat_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['repeat_password']:
            raise forms.ValidationError('Passwords don\'t match!!!')

    def clean_email(self):
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
            raise forms.ValidationError('E-mail already in use!!!')
        except User.DoesNotExist:
            return self.cleaned_data['email']

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'],
                                        first_name=self.cleaned_data['first_name'],
                                        last_name=self.cleaned_data['last_name'],
                                        email=self.cleaned_data['email'],
                                        password=self.cleaned_data['password'],
                                        )
        Profile.objects.create(user=user)
        return authenticate(username=self.cleaned_data['username'],
                            password=self.cleaned_data['password'],
                            )


class QuestionForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', }
        ),
        min_length=3,
        max_length=100,
        label='Title',
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', }
        ),
        label='Text',
    )
    tags = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', }
        ),
        label='Tags',
    )

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        forms.Form.__init__(self, *args, **kwargs)

    def clean_title(self):
        try:
            question = Question.objects.get(title=self.cleaned_data['title'])
            raise forms.ValidationError('Title is already in use!!!')
        except Question.DoesNotExist:
            return self.cleaned_data['title']

    def clean_tags(self):
        if 'tags' in self.cleaned_data:

            if self.cleaned_data['tags'].count(',') > 2:
                raise forms.ValidationError('Can\'t be more than 3 tags!!!')

            return self.cleaned_data['tags']

    def save(self):
        question = Question()

        question.title = self.cleaned_data['title']
        question.text = self.cleaned_data['text']
        print(self.cleaned_data['text'])
        question.author = Profile.objects.all()[0]
        print(question.author)
        question.date = datetime.now()
        question.likes = 0

        question.save()

        if 'tags' in self.cleaned_data:

            for tag in self.cleaned_data['tags'].split(' '):

                if len(tag):
                    print(tag)
                    if len(Tag.objects.filter(title=tag)) == 0:
                        t = Tag()
                        t.title = tag
                        t.save()
                    t = Tag.objects.get(title=tag)

                    question.tags.add(t)

        return question


class AnswerForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'class':'form-control', 'rows':'4', 'id':"comment", 'placeholder':"Enter you answer here", 'style': 'width: 100%; max-height: 200px;'}
        ),
        label='Text',
    )

    def __init__(self, user=None, question_id=None, *args, **kwargs):
        self.user = user
        self.question_id = question_id
        forms.Form.__init__(self, *args, **kwargs)

    def clean_text(self):
        return self.cleaned_data['text']

    def save(self):
        answer = Answer()
        answer.text = self.cleaned_data['text']
        answer.question = Question.objects.get(id=self.question_id)
        answer.author = Profile.objects.get(user=self.user)
        answer.save()
        return answer.question


class PollForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', }
        ),
        min_length=3,
        max_length=100,
        label='Title',
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', }
        ),
        label='Text',
    )

    def get_text(self):
        begin = self.cleaned_data['text'].find('<text>')
        end = self.cleaned_data['text'].find('</text>')
        if begin == -1 or end == -1:
            return None
        return self.cleaned_data['text'][begin+len('<text>'):end]

    """
<text> Some text </text>
<answer> First answer </answer>
<poll>poll1</poll>
<poll>poll2</poll>
<poll>poll3</poll>
<answer> Second answer </answer>
<poll>poll2-1</poll>
<poll>poll2-2</poll>
<poll>poll2-3</poll>
    """

    def get_polls(self):
        titles = list()
        polls = list()
        first = self.cleaned_data['text'].find('<answer>')
        second = self.cleaned_data['text'].find('</answer>')
        while first != -1 or second != -1:
            print('1 - ', first, ' ', second)
            next_ans = self.cleaned_data['text'].find('<answer>', second)
            titles.append(self.cleaned_data['text'][first+len('<answer>'):second])
            poll_vars = list()
            first_poll = self.cleaned_data['text'].find('<poll>', second)
            second_poll = self.cleaned_data['text'].find('</poll>', second)
            while first_poll != -1 or second_poll != -1:
                if next_ans != -1 and (first_poll > next_ans or second_poll > next_ans):
                    break
                print('2 - ', first, ' ', second)
                poll_vars.append(self.cleaned_data['text'][first_poll+len('<poll>'):second_poll])
                first_poll = self.cleaned_data['text'].find('<poll>', second_poll)
                second_poll = self.cleaned_data['text'].find('</poll>', second_poll+1)

            polls.append(poll_vars)
            first = self.cleaned_data['text'].find('<answer>', second+1)
            second = self.cleaned_data['text'].find('</answer>', second+1)

        print('titles = ', titles)
        print('polls = ', polls)
        return titles, polls

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        forms.Form.__init__(self, *args, **kwargs)

    def clean_title(self):
        return self.cleaned_data['title']

    def clean_text(self):
        return self.cleaned_data['text']

    def save(self):
        poll_text = self.get_text()
        titles, polls = self.get_polls()

        answer = AnswerPoll()
        answer.title = self.cleaned_data['title']
        answer.text = poll_text
        answer.author = Profile.objects.get(user=self.user)
        answer.save()

        for i in range(len(titles)):
            poll = Poll()
            poll.answer_poll = AnswerPoll.objects.get(id=answer.id)
            poll.answer = titles[i]
            poll.save()
            for j in range(len(polls[i])):
                poll_var = PollVariant()
                poll_var.poll = Poll.objects.get(id=poll.id)
                poll_var.text = polls[i][j]
                poll_var.save()

        return answer