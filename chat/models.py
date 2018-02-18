import json,os
from django.db import models
from django.utils.six import python_2_unicode_compatible

from AuthSer.models import User

import channels
from .settings import MSG_TYPE_MESSAGE

# TODO group app 으로 이동
class Group(models.Model):
    group_name = models.CharField(max_length=50, null=False)  # group_name 입력은 필수로 한다.

    manager_id = models.ForeignKey(
        User,
        related_name="groupManagers",
        on_delete=models.CASCADE,
        null=False
    )

    class Meta:
        verbose_name = "group"
        verbose_name_plural = "groups"

    # def __str__(self):
    #    return self.group_name

    # # 이 그룹의 모든 토픽을 가져온다.
    # def get_topic(self):
    #     return self.topics.all()


# TODO group app 으로 이동
class GroupMember(models.Model):
    """
    어떤 그룹에 어떤 사용자가 있는지
    """
    group_id = models.ForeignKey(
        Group,
        related_name="groupMembers",
        on_delete=models.CASCADE
    )
    user_id = models.ForeignKey(
        User,
        related_name="groupMembers",
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(
        null=False,
        default=False
    )

    def __str__(self):
        return str(self.group_id)


##############################################################################################

@python_2_unicode_compatible
class Topic(models.Model):
    """
    A topic for people to chat in.
    """
    topic_name = models.CharField(max_length=50, blank=True, null=False, default='main-topic')
    group_id = models.ForeignKey(
        Group,
        related_name="topics",
        on_delete=models.CASCADE,
    )
    created_time = models.DateTimeField('Create Time', auto_now_add=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.topic_name

    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        print("============group_name============" + str(self.id))
        return "room-%s" % self.id


@python_2_unicode_compatible
class TopicMember(models.Model):
    user_id = models.ForeignKey(
        User,
        related_name="topics"
    )
    topic_id = models.ForeignKey(
        Topic,
        related_name="topics"
    )
    created_time = models.DateTimeField('Create Time', auto_now_add=True)

    def __str__(self):
        return '[{user_id}] {topic_id}'.format(**self.as_dict())

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'topic_id': self.topic_id,
        }


@python_2_unicode_compatible
class TopicMessage(models.Model):
    user_id = models.ForeignKey(
        User,
        related_name="topic_messages"
    )
    topic_id = models.ForeignKey(
        Topic,
        related_name="topic_messages"
    )
    contents = models.TextField()  # 메시지 내용
    is_file = models.BooleanField(default=False)  # file이면 True
    created_time = models.DateTimeField('Create Time', auto_now_add=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return '[{user_id}] {topic_id}: {created_time}'.format(**self.as_dict())

    @property
    def formatted_created_time(self):
        return self.created_time.strftime('%b %-d %-I:%M %p')

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'topic_id': self.topic_id,
            'created_time': self.formatted_created_time
        }

##############################################################################################


@python_2_unicode_compatible
class ChatRoom(models.Model):
    """
    A chat for people to chat in.
    """
    group = models.ForeignKey(
        Group,
        related_name="chatRooms",
        on_delete=models.CASCADE,
    )
    created_time = models.DateTimeField('Create Time', auto_now_add=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return '[{pk}] {group}'.format(**self.as_dict())

    def as_dict(self):
        return {
            'pk': self.pk,
            'group': self.group,
        }

    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        print("============group_name============" + str(self.id))
        return "room-%s" % self.id

    # 해당 채팅방의 모든 ChatMember를 가져온다 (이 멤버들의 이름이 곧 채팅방의 이름)
    def get_chatRoomMembers(self):
        queryset = self.chatRoomMembers.filter(chatRoom=self.pk)
        return queryset

    # 해당 채팅방의 모든 Messages를 가져온다
    def get_messages(self):
        print("ChatRoom -- get_all_messages")
        print(self.chatRoomMessages.all())
        return self.chatRoomMessages.all()


@python_2_unicode_compatible
class ChatRoomMember(models.Model):
    user = models.ForeignKey(
        User,
        related_name="chatRoomMembers"
    )
    chatRoom = models.ForeignKey(
        ChatRoom,
        related_name="chatRoomMembers"
    )
    created_time = models.DateTimeField('Create Time', auto_now_add=True)

    def __str__(self):
        return '[{user}] {chatRoom}'.format(**self.as_dict())

    def as_dict(self):
        return {
            'user': self.user,
            'chatRoom': self.chatRoom,
        }


@python_2_unicode_compatible
class ChatRoomMessage(models.Model):
    user = models.ForeignKey(
        User,
        related_name="chatRoomMessages"

    )
    chatRoom = models.ForeignKey(
        ChatRoom,
        related_name="chatRoomMessages"
    )
    contents = models.TextField()  # 메시지 내용
    created_time = models.DateTimeField('Create Time', auto_now_add=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return '[{user}] {chatRoom}: {created_time}'.format(**self.as_dict())

    @property
    def formatted_created_time(self):
        return self.created_time.strftime('%b %-d %-I:%M %p')

    def as_dict(self):
        return {
            'user': self.user,
            'chatRoom': self.chatRoom,
            'created_time': self.formatted_created_time
        }


#########################################################################################

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
    created_time = models.DateTimeField('Create Time', auto_now_add=True)

    def get_filename(self):
        filename = os.path.basename(self.file.name)
        print("[[TopicFile]] get_filename")
        print(filename)
        return filename