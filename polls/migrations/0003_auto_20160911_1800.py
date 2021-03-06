# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-11 18:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_poll_multi'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailEnter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(default='email', max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Poll')),
            ],
        ),
        migrations.CreateModel(
            name='TextEnter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=30)),
                ('text', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TextPoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500)),
                ('survey', models.ManyToManyField(to='polls.Survey')),
            ],
        ),
        migrations.RemoveField(
            model_name='emailchoice',
            name='poll',
        ),
        migrations.DeleteModel(
            name='EmailChoice',
        ),
        migrations.AddField(
            model_name='textenter',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.TextPoll'),
        ),
    ]
