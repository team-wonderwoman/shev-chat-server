# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-17 11:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AuthSer', '0001_initial'),
        ('chat', '0005_remove_fileupload_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Create Time')),
            ],
        ),
        migrations.DeleteModel(
            name='FileUpload',
        ),
        migrations.AddField(
            model_name='topicmessage',
            name='is_file',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='topicfile',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic_files', to='chat.TopicMessage'),
        ),
        migrations.AddField(
            model_name='topicfile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic_files', to='AuthSer.User'),
        ),
    ]
