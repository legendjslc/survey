# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-19 21:04
from __future__ import unicode_literals

import adminsortable.fields
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0017_survey_the_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='charchoice',
            options={'ordering': ['the_order'], 'verbose_name_plural': 'Choices'},
        ),
        migrations.AlterModelOptions(
            name='survey',
            options={'ordering': ['the_order'], 'verbose_name_plural': 'Surveys'},
        ),
        migrations.AlterField(
            model_name='charchoice',
            name='poll',
            field=adminsortable.fields.SortableForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Poll'),
        ),
    ]
