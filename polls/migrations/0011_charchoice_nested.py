# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-14 21:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_auto_20160914_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='charchoice',
            name='nested',
            field=models.ManyToManyField(related_name='nesting_choices', to='polls.Poll'),
        ),
    ]