from django.contrib import admin
from .models import (
    Group, GroupMember,
    ChatRoom, ChatRoomMember, ChatRoomMessage,
    Topic, TopicMessage
)
from AuthSer.models import User

admin.site.register(User)

admin.site.register(Group)
admin.site.register(GroupMember)

admin.site.register(Topic)
# admin.site.register(TopicMember)
admin.site.register(TopicMessage)

admin.site.register(ChatRoom)
admin.site.register(ChatRoomMember)
admin.site.register(ChatRoomMessage)