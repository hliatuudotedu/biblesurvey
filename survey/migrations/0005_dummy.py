# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-13 04:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_provider_survey_surveyquestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dummy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dummy', models.CharField(max_length=100)),
            ],
        ),
    ]