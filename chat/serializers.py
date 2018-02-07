from .models import Group, GroupMember
# from .models import ChatRoom, ChatMember, Message
from .models import Topic, TopicMessage, TopicMember
from shevauthserver.models import User
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    HyperlinkedModelSerializer,
    HyperlinkedIdentityField
)


class GroupListSerializer(ModelSerializer):
    group_name = SerializerMethodField()

    class Meta:
        model = Group
        fields = ('group_name', )

    def get_group_name(self, obj):
        return obj.values('group_name')


####################################################################

# 해당 토픽의 detail로 연결
topic_detail_url = HyperlinkedIdentityField(
    view_name='topic_detail',
)


class TopicListSerializer(ModelSerializer):

    class Meta:
        model = Topic
        fields = ('topic_name', )


class TopicDetailSerializer(ModelSerializer):
    # messages = TopicMessage.

    class Meta:
        model = Topic
        fields = ('topic_name', 'created_time')
