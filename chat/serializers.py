from .models import Group, GroupMember
from .models import Topic, TopicMessage, TopicMember
from .models import ChatRoom, ChatRoomMember, ChatRoomMessage
from shevauthserver.models import User

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