# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-07 15:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CharChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='EmailChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=1000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filled', models.DateTimeField(auto_now_add=True)),
                ('choices', models.ManyToManyField(to='polls.CharChoice')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Survey')),
            ],
        ),
        migrations.AddField(
            model_name='poll',
            name='survey',
            field=models.ManyToManyField(to='polls.Survey'),
        ),
        migrations.AddField(
            model_name='emailchoice',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Poll'),
        ),
        migrations.AddField(
            model_name='charchoice',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Poll'),
        ),
    ]
