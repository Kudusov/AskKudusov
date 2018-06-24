# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-14 00:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0008_conversation_personalmessages'),
    ]

    operations = [
        migrations.CreateModel(
            name='UniversalQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('likes', models.IntegerField(default=0)),
                ('type', models.CharField(choices=[('Q', 'Question'), ('A', 'Answer'), ('P', 'QuestionPoll')], max_length=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ask.Profile')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ask.UniversalQuestion')),
                ('tags', models.ManyToManyField(to='ask.Tag')),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
    ]