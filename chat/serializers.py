from rest_framework import serializers
from .models import Group, GroupMember

# from .models import ChatRoom, ChatMember, Message
from AuthSer.models import User

from .models import Topic, TopicMessage
from .models import ChatRoom, ChatRoomMember, ChatRoomMessage
from rest_framework.renderers import JSONRenderer

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    HyperlinkedModelSerializer,
    HyperlinkedIdentityField
)


class GroupListSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'group_name', 'manager_id', )  #__all__


class GroupMemberModelSerializer(ModelSerializer):
    class Meta:
        model = GroupMember
        fields = ('id', 'group_id', 'user_id', 'is_active', )  #__all__
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


# class TopicMemberSerializer(ModelSerializer):
#     class Meta:
#         model = TopicMember
#         fields = '__all__'  # user_id, topic_id


class TopicMessageSerializer(ModelSerializer):
    sender = SerializerMethodField()

    class Meta:
        model = TopicMessage
        fields = ('sender', 'topic_id', 'contents', 'created_time')

    def get_sender(self, obj):
        return obj.user_id.user_name


####################################################################

# 해당 채팅방의 detail로 연결
chatRoom_detail_url = HyperlinkedIdentityField(
    view_name='chatRoom_detail',
)


class ChatRoomListSerializer(ModelSerializer):
    chatRoomMember_name = SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ('id', 'chatRoomMember_name', )

    # chatRoomMeber_name을 리스트로 보내서 채팅방 이름으로 세팅한다
    def get_chatRoomMember_name(self, obj):
        print("[[ChatRoomListSerializer]] get_chatRoomMember_name -----")
        queryset = obj.get_chatRoomMembers()  # 해당 채팅방의 ChatRoomMember에 대한 queryset
        serializer = ChatRoomMemberSerializer(queryset, many=True)

        return serializer.data


class ChatRoomDetailSerializer(ModelSerializer):
    chatRoomMember_name = SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ('id', 'chatRoomMember_name', 'created_time')

    # chatRoomMeber_name을 리스트로 보내서 채팅방 이름으로 세팅한다
    def get_chatRoomMember_name(self, obj):
        print("[[ChatRoomListSerializer]] get_chatRoomMember_name -----")
        queryset = obj.get_chatRoomMembers()  # 해당 채팅방의 ChatRoomMember에 대한 queryset
        serializer = ChatRoomMemberSerializer(queryset, many=True)

        return serializer.data


# 해당하는 채팅방의 멤버 이름을 반환
class ChatRoomMemberSerializer(ModelSerializer):
    member_name = SerializerMethodField()

    class Meta:
        model = ChatRoomMember
        fields = ('member_name', )

    def get_member_name(self, obj):
        return obj.user.user_name


class ChatRoomMessageSerializer(ModelSerializer):
    sender = SerializerMethodField()

    class Meta:
        model = ChatRoomMessage
        fields = ('sender', 'chatRoom', 'contents', 'created_time')

    def get_sender(self, obj):
        return obj.user.user_name