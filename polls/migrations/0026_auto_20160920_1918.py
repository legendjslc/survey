# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-20 19:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0025_charchoice_created_by_visitor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charchoice',
            name='created_by_visitor',
            field=models.BooleanField(default=False),
        ),
    ]
