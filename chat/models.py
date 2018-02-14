import json
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

    # @property
    # def websocket_group(self):
    #     """
    #     Returns the Channels Group that sockets should subscribe to to get sent
    #     messages as they are generated.
    #     """
    #     return channels.Group("room-%s" % self.id)  # channels group
    #
    # # 방에 join/leave하거나 message를 보낼 때 client에 전달하는 json data
    # def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
    #     """
    #     Called to send a message to the room on behalf of a user.
    #     """
    #     final_msg = {'room': str(self.id), 'message': message, 'username': user.username, 'msg_type': msg_type}
    #
    #     # Send out the message to everyone in the room
    #     self.websocket_group.send(
    #         {"text": json.dumps(final_msg)}
    #     )


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


# @python_2_unicode_compatible
# class ChatRoom(models.Model):
#     """
#     A chat for people to chat in.
#     """
#     chatroom_name = models.CharField(max_length=50, blank=True, null=False, default='main-topic')
#     group_id = models.ForeignKey(
#         Group,
#         related_name="topics",
#         on_delete=models.CASCADE,
#     )
#     created_time = models.DateTimeField('Create Time', auto_now_add=True)
#
#     class Meta:
#         ordering = ['-created_time']
#
#     def __str__(self):
#         return self.topic_name
#
#     @property
#     def group_name(self):
#         """
#         Returns the Channels Group name that sockets should subscribe to to get sent
#         messages as they are generated.
#         """
#         print("============group_name============" + str(self.id))
#         return "room-%s" % self.id
#
#         # @property
#         # def websocket_group(self):
#         #     """
#         #     Returns the Channels Group that sockets should subscribe to to get sent
#         #     messages as they are generated.
#         #     """
#         #     return channels.Group("room-%s" % self.id)  # channels group
#         #
#         # # 방에 join/leave하거나 message를 보낼 때 client에 전달하는 json data
#         # def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
#         #     """
#         #     Called to send a message to the room on behalf of a user.
#         #     """
#         #     final_msg = {'room': str(self.id), 'message': message, 'username': user.username, 'msg_type': msg_type}
#         #
#         #     # Send out the message to everyone in the room
#         #     self.websocket_group.send(
#         #         {"text": json.dumps(final_msg)}
#         #     )
#
# @python_2_unicode_compatible
# class TopicMember(models.Model):
#     user_id = models.ForeignKey(
#         User,
#         related_name="topics"
#     )
#     topic_id = models.ForeignKey(
#         Topic,
#         related_name="topics"
#     )
#     created_time = models.DateTimeField('Create Time', auto_now_add=True)
#
#     def __str__(self):
#         return '[{user_id}] {topic_id}'.format(**self.as_dict())
#
#     def as_dict(self):
#         return {
#             'user_id': self.user_id,
#             'topic_id': self.topic_id,
#         }
#
# @python_2_unicode_compatible
# class TopicMessage(models.Model):
#     user_id = models.ForeignKey(
#         User,
#         related_name="topic_messages"
#     )
#     topic_id = models.ForeignKey(
#         Topic,
#         related_name="topic_messages"
#     )
#     contents = models.TextField()  # 메시지 내용
#     created_time = models.DateTimeField('Create Time', auto_now_add=True)
#
#     class Meta:
#         ordering = ['-created_time']
#
#     def __str__(self):
#         return '[{user_id}] {topic_id}: {created_time}'.format(**self.as_dict())
#
#     @property
#     def formatted_created_time(self):
#         return self.created_time.strftime('%b %-d %-I:%M %p')
#
#     def as_dict(self):
#         return {
#             'user_id': self.user_id,
#             'topic_id': self.topic_id,
#             'created_time': self.formatted_created_time
#         }
# @python_2_unicode_compatible
# class ChatRoom(models.Model):
#     """
#     A room for people to chat in.
#     """
#     group_id = models.ForeignKey(
#         Group,
#         related_name="chatRooms"
#     )
#     created_time = models.DateTimeField('Create Time', auto_now_add=True)
#
#     class Meta:
#         ordering = ['-created_time']
#
#     # 해당 채팅룸의 모든 Message를 가져온다.
#     def get_message(self):
#         return self.message.all()
#
#     # 해당 채팅룸의 모든 ChatMember를 가져온다.
#     def get_chat_member(self):
#         return self.chatMember.all()
#
#
# @python_2_unicode_compatible
# class ChatMember(models.Model):
#     user_id = models.ManyToManyField(User)
#     chat_room_id = models.ManyToManyField(
#         ChatRoom,
#         related_name="chatMembers"
#     )
#     created_time = models.DateTimeField('Create Time', auto_now_add=True)
#
#
# @python_2_unicode_compatible
# class Message(models.Model):
#     user_id = models.ManyToManyField(
#         User,
#         related_name="messages"
#     )
#     chat_room_id = models.ManyToManyField(
#         ChatRoom,
#         related_name="messages"
#     )
#     contents = models.TextField()  # 메시지 내용
#     created_time = models.DateTimeField('Create Time', auto_now_add=True)
#
#     class Meta:
#         ordering = ['-created_time']
#
#     def __str__(self):
#         return '[{user_id}] {chat_room_id}: {created_time}'.format(**self.as_dict())
#
#     @property
#     def formatted_created_time(self):
#         return self.created_time.strftime('%b %-d %-I:%M %p')
#
#     def as_dict(self):
#         return {
#             'user_id': self.user_id,
#             'chat_room_id': self.chat_room_id,
#             'created_time': self.formatted_created_time
#         }