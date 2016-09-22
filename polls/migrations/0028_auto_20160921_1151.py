# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-21 11:51
from __future__ import unicode_literals

import adminsortable.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0027_surveyattribute'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='surveyattribute',
            options={'ordering': ['attr_order'], 'verbose_name_plural': 'Survey Attributes'},
        ),
        migrations.AddField(
            model_name='surveyattribute',
            name='attr_order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='surveyattribute',
            name='survey',
            field=adminsortable.fields.SortableForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Survey'),
        ),
    ]