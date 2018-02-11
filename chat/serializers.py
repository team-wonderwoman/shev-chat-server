from .models import Group, GroupMember
# from .models import ChatRoom, ChatMember, Message
from .models import Topic, TopicMessage, TopicMember, User
from shevauthserver.models import User
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    HyperlinkedModelSerializer,
    HyperlinkedIdentityField
)


class GroupListSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('group_name', )


####################################################################

# 해당 토픽의 detail로 연결
topic_detail_url = HyperlinkedIdentityField(
    view_name='topic_detail',
)


class TopicListSerializer(ModelSerializer):

    class Meta:
        model = Topic
        fields = ('id', 'topic_name', )


class TopicDetailSerializer(ModelSerializer):
    # messages = TopicMessageSerializer()

    class Meta:
        model = Topic
        fields = ('id', 'topic_name', 'created_time')


class TopicMessageSerializer(ModelSerializer):
    sender = SerializerMethodField()

    class Meta:
        model = TopicMessage
        fields = ('sender', 'topic_id', 'contents', 'created_time')

    def get_sender(self, obj):
        return obj.user_id.user_name
