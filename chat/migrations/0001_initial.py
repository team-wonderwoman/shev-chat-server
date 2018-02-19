# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-19 07:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AuthSer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Create Time')),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='ChatRoomMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Create Time')),
                ('chatRoom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatRoomMembers', to='chat.ChatRoom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatRoomMembers', to='AuthSer.User')),
            ],
        ),
        migrations.CreateModel(
            name='ChatRoomMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Create Time')),
                ('chatRoom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatRoomMessages', to='chat.ChatRoom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatRoomMessages', to='AuthSer.User')),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=50)),
                ('manager_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupManagers', to='AuthSer.User')),
            ],
            options={
                'verbose_name': 'group',
                'verbose_name_plural': 'groups',
            },
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupMembers', to='chat.Group')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupMembers', to='AuthSer.User')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_name', models.CharField(blank=True, default='main-topic', max_length=50)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Create Time')),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='chat.Group')),
            ],
            options={
                'ordering': ['created_time'],
            },
        ),
        migrations.CreateModel(
            name='TopicFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('origin_filename', models.TextField(blank=True)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Create Time')),
            ],
        ),
        migrations.CreateModel(
            name='TopicMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.TextField()),
                ('is_file', models.BooleanField(default=False)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Create Time')),
                ('topic_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic_messages', to='chat.Topic')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic_messages', to='AuthSer.User')),
            ],
            options={
                'ordering': ['-created_time'],
            },
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
        migrations.AddField(
            model_name='chatroom',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatRooms', to='chat.Group'),
        ),
    ]
