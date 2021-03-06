# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-13 19:55
from __future__ import unicode_literals

import adminsortable.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0056_auto_20161013_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charchoice',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='polls.ChoiceGroup'),
        ),
        migrations.AlterField(
            model_name='charchoice',
            name='poll',
            field=adminsortable.fields.SortableForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='polls.Poll'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='polls.PollGroup'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='survey',
            field=adminsortable.fields.SortableForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='polls.Survey'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='newsletter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='survey_newsletter', to='polls.Elmail'),
        ),
        migrations.AlterField(
            model_name='surveyattribute',
            name='survey',
            field=adminsortable.fields.SortableForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='polls.Survey'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='collected_data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='polls.Dicty'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='survey',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='polls.Survey'),
        ),
    ]
