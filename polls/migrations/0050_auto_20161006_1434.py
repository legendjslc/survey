# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-06 14:34
from __future__ import unicode_literals

import adminsortable.fields
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0049_auto_20161006_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charchoice',
            name='poll',
            field=adminsortable.fields.SortableForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Poll'),
        ),
    ]
