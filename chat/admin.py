from django.contrib import admin
from .models import (
    Group, GroupMember,
    # ChatRoom, ChatMember, Message,
    Topic, TopicMember, TopicMessage
)
from shevauthserver.models import User

admin.site.register(User)

admin.site.register(Group)
admin.site.register(GroupMember)
# admin.site.register(ChatRoom)
# admin.site.register(ChatMember)
# admin.site.register(Message)
admin.site.register(Topic)
admin.site.register(TopicMember)
admin.site.register(TopicMessage)
