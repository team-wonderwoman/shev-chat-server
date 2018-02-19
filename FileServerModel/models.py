import os
from django.db import models
from django.utils.six import python_2_unicode_compatible

# from ChatServerModel.models import *
# from AuthServerModel.models import User

from chat.models import TopicMessage, ChatRoomMember, ChatRoomMessage, ChatRoom, Topic, GroupMember, Group
from AuthSer.models import User


@python_2_unicode_compatible
class TopicFile(models.Model):
    user = models.ForeignKey(
        User,
        related_name="topic_files"
    )
    message = models.ForeignKey(
        TopicMessage,
        related_name="topic_files"
    )
    file = models.FileField()
    origin_filename = models.TextField(null=False, blank=True)
    created_time = models.DateTimeField('Create Time', auto_now_add=True)

    def get_origin_filename(self):
        return self.origin_filename

    def get_filename(self):
        filename = os.path.basename(self.file.name)
        print("[[TopicFile]] get_filename")
        print(filename)
        return filename


@python_2_unicode_compatible
class ChatRoomFile(models.Model):
    user = models.ForeignKey(
        User,
        related_name="chatRoom_files"
    )
    message = models.ForeignKey(
        ChatRoomMessage,
        related_name="chatRoom_files"
    )
    file = models.FileField()
    origin_filename = models.TextField(null=False, blank=True)
    created_time = models.DateTimeField('Create Time', auto_now_add=True)

    def get_origin_filename(self):
        return self.origin_filename

    def get_filename(self):
        filename = os.path.basename(self.file.name)
        print("[[ChatRoomFile]] get_filename")
        print(filename)
        return filename