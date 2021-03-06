# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-14 01:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0009_universalquestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='UniversalQuestionLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ask.Profile')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ask.UniversalQuestion')),
            ],
        ),
    ]
