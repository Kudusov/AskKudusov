# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-13 20:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerPoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ask.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=30)),
                ('answer_poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ask.AnswerPoll')),
            ],
        ),
        migrations.CreateModel(
            name='PollVariant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=30)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ask.Poll')),
            ],
        ),
    ]
