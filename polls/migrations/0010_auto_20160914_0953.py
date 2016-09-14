# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-14 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20160914_0753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textenter',
            name='poll',
        ),
        migrations.RemoveField(
            model_name='textpoll',
            name='survey',
        ),
        migrations.RemoveField(
            model_name='visitor',
            name='textentries',
        ),
        migrations.AlterField(
            model_name='poll',
            name='poll_type',
            field=models.CharField(choices=[('multi', 'pick multiple options'), ('one', 'pick one option'), ('countries', 'pick a country from the list'), ('text', 'type text')], default='multi', max_length=30),
        ),
        migrations.DeleteModel(
            name='TextEnter',
        ),
        migrations.DeleteModel(
            name='TextPoll',
        ),
    ]
