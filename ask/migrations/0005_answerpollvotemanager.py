# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-14 10:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0004_auto_20180514_0947'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerPollVoteManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
