# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 22:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0071_auto_20161024_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='notify',
            field=models.BooleanField(default=False),
        ),
    ]
