# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-10 06:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=45)),
                ('user_name', models.CharField(max_length=45)),
                ('user_tel', models.CharField(blank=True, max_length=45)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
