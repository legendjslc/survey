# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-21 22:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0030_auto_20160921_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='include_in_details',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='visitor',
            name='include_raport',
            field=models.BooleanField(default=True),
        ),
    ]
