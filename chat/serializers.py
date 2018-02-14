from rest_framework import serializers
from .models import Group, GroupMember
# from .models import ChatRoom, ChatMember, Message
from AuthSer.models import User
from .models import Topic, TopicMessage, TopicMember
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    HyperlinkedModelSerializer,
    HyperlinkedIdentityField
)

class GroupListSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('id','group_name','manager_id', ) #__all__


class GroupMemberModelSerializer(ModelSerializer):
    class Meta:
        model = GroupMember
        fields = ('id', 'group_id','user_id','is_active', ) #__all__
    #
    # def create(self, validated_data):
    #     group_id = validated_data.pop('group_id')
    #     members = validated_data.pop('members')
    #     user_id = validated_data.pop('user_id')
    #     is_active = validated_data.pop('is_active')
    #     group_member = GroupMember.objects.create(**validated_data)
    #     return group_member


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
