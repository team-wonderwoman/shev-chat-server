from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
#
# import json
# from django.core.serializers.json import DjangoJSONEncoder
# from django.http import JsonResponse
#
#
# from rest_framework.parsers import JSONParser
# from rest_framework import serializers
# from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
#
#
# from rest_framework.permissions import (
#     AllowAny,
#     IsAuthenticated,
#     IsAdminUser,
#     IsAuthenticatedOrReadOnly,
# )
#
# from .permissions import IsOwnerOrReadOnly

from .models import Group, GroupMember, Topic, ChatRoom, ChatRoomMember
from shevauthserver.models import User

from .serializers import (
    GroupListSerializer,
    TopicListSerializer,
    TopicDetailSerializer,
    TopicMessageSerializer,
    ChatRoomListSerializer,
    ChatRoomDetailSerializer,
    ChatRoomMessageSerializer,
    ChatRoomMemberSerializer,
)
## for file
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView


## for test
# @login_required
def index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered group_id
    # json post로 넘겨준 group_id에 해당하는 topic, chat list를 넘겨준다.
    rooms = Topic.objects.filter(group_id=1).order_by("group_id")
    print(rooms)

    # Rende
    # r that in the index template
    return render(request, "index.html", {
        "rooms": rooms,
    })


# 로그인한 사용자의 GroupMember List 를 반환
# @method_decorator(login_required, name='dispatch')
class GroupListAPIView(ListAPIView):
    serializer_class = GroupListSerializer

    def get(self, *args, **kwargs):
        # queryset = GroupMember.objects.all()
        # qs = Group.objects.all()
        user_id = self.kwargs['user_id']  # url에 있는 user_id를 가져온다
        print(user_id)

        if user_id is not None:
            # queryset = queryset.filter(user_id=user_id)  # user가 속한 group을 가져온다
            queryset = GroupMember.objects.filter(user_id=user_id)
            # qs = qs.filter(pk__in=queryset.values('group_id'))  # 해당 group의 name을 가져온다
            qs = Group.objects.filter(pk__in=queryset.values('group_id'))
            serializer = GroupListSerializer(qs)
            print(serializer.data)
            return Response(serializer.data)


class GroupDetailAPIView(APIView):

    # user가 속한 그룹의 Topic, Chat list를 반환한다
    def get(self, *args, **kwargs):
        print("groupdetailapiview")
        group_id = self.kwargs['group_id']
        queryset1 = Topic.objects.filter(group_id=group_id).order_by('pk')
        queryset2 = ChatRoom.objects.filter(group_id=group_id).order_by('pk')
        serializer1 = TopicListSerializer(queryset1, many=True)
        serializer2 = ChatRoomListSerializer(queryset2, many=True)

        response_json_data = {
            'topic_serializer': serializer1.data,
            'chatroom_serializer': serializer2.data,
        }
        return Response(response_json_data)

##########################################################################


class TopicListViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicListSerializer

    # list [GET] 해당 그룹의 토픽 리스트 조회
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = TopicListSerializer(queryset, many=True)  # 해당 group의 모든 topic_name을 가져온다
        return Response(serializer.data)

    # list [POST] 해당 그룹의 토픽 생성, POST로 토픽 이름 설정
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override
    # url에 입력한 group_id에 해당하는 Topic query set을 반환
    def get_queryset(self):
        group_id = self.kwargs['group_id']  # data in url
        print("group_id:" + str(group_id))

        return Topic.objects.filter(group_id=group_id)

    # override
    # url에 입력한 group_id에 해당하는 Topic에 POST로 넘어온 topic_name을 세팅 후 save
    def perform_create(self, serializer):
        topic_name = self.request.data['topic_name']  # data in POST body
        print("topic_name: " + str(topic_name))

        group_id = self.kwargs['group_id']
        group = Group.objects.get(pk=group_id)

        serializer.save(group_id=group, topic_name=topic_name)


class TopicDetailViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicDetailSerializer

    # detail [GET] 토픽 안의 내용 및 파일정보 가져오기
    def retrieve(self, request, *args, **kwargs):
        """
        Room view - show the topic, with latest topicmessages.
        The template for this view has the WebSocket business to send and stream message,
        so see the template for wherer the magic happens.
        """
        # If the room with the given topic_id doesn't exist, automatically create it
        # upon first visit
        topic_id = self.kwargs['topic_id']
        print("topic_id: " + str(topic_id))

        topic, created = Topic.objects.get_or_create(pk=topic_id)
        topic_serializer = TopicDetailSerializer(topic)

        topic_message = topic.topic_messages.order_by('created_time')[:50]
        topic_message_serializer = TopicMessageSerializer(topic_message, many=True)

        # We want to show the last 100 messages, ordered most-recent-last
        # topic_message = reversed(topic_message_serializer)

        # url에 입력한 topic_id에 해당하는 Topic Serializer와 해당 topic의 기존 message들을 가져온다
        response_json_data = {
            # 'topic': topic,
            'topic_serializer': topic_serializer.data,
            'topic_message_serializer': topic_message_serializer.data,
        }

        return Response(response_json_data)

    # detail [PUT] 토픽 이름 변경
    def update(self, request, *args, **kwargs):
        qs = self.get_queryset()

        serializer = TopicDetailSerializer(
            qs,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # detail [DELETE] 토픽 삭제(기본 토픽은 삭제 불가)
    def destroy(self, request, *args, **kwargs):
        topic_id = self.kwargs['topic_id']
        topic = self.get_object(topic_id)
        topic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # override
    # pk에 해당하는 Topic obj를 반환
    def get_object(self, pk):
        try:
            return Topic.objects.get(pk=pk)
        except Topic.DoesNotExist:
            raise Http404  ### TODO error 수정 필요

    # override
    # url에 입력한 topic_id에 해당하는 Topic query set을 반환
    def get_queryset(self):
        topic_id = self.kwargs['topic_id']  # data in url
        print("topic_id:" + str(topic_id))

        return Topic.objects.get(pk__in=topic_id)

##########################################################################


class ChatRoomListViewSet(ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomListSerializer

    # list [GET] 해당 그룹의 '자신이 속한' 채팅방 리스트 조회
    def list(self, request, *args, **kwargs):
        # user_id = self.kwargs['user_id']  # url에 있는 user_id를 가져온다
        user_id = 1  # TODO
        group_id = self.kwargs['group_id']  # url에 있는 group_id를 가져온다
        print("user_id: " + str(user_id) + ", group_id: " + str(group_id))

        if user_id is not None:
            # ChatRoomMember에서 해당 사용자가 속한 ChatRoomMember query를 가져온다
            chatRoomMember_queryset = ChatRoomMember.objects.filter(user=user_id)  # user가 속한 chatroom을 가져온다

            # ChatRoomMember query에서 ChatRoom pk를 이용해 해당 ChatRoom query를 모두 가져온다
            # 해당 ChatRoom에서 user가 현재 들어온 group에 속한 ChatRoom만을 반환한다
            chatRoom_queryset = ChatRoom.objects.filter(pk__in=chatRoomMember_queryset.values('chatRoom'), group=group_id)

            serializer = ChatRoomListSerializer(chatRoom_queryset, many=True)  # 자신이 속한 chatRoom를 가져온다
            return Response(serializer.data)

    # list [POST] 해당 그룹의 채팅방 생성, POST로 채팅방의 멤버로 등록
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)  # 채팅방을 생성

        # 채팅방을 생성한 사람을 ChatRoomMember로 추가한다
        creater_id = self.request.data['createrID']  # data in POST body
        creater = User.objects.get(pk=creater_id)

        chatRoom = ChatRoom.objects.get(pk=serializer.data['id'])  # serializer.data 사용
        print("createrID: " + str(creater_id) + ", chatRoom: " + str(chatRoom))
        chatroommember_serializer = ChatRoomMemberSerializer(data=self.request.data)
        chatroommember_serializer.is_valid(raise_exception=True)
        chatroommember_serializer.save(user=creater, chatRoom=chatRoom)
        print("추가된 chatroommember")
        print(serializer.get_chatRoomMember_name(chatRoom))  # 추가된 chatroommember dict

        # TODO 생성한 채팅방을 다시 업데이트 (chatroommember을 적용하기 위해)

        # print(serializer.get_chatRoomMember_name(chatRoom))  # 추가된 chatroommember dict
        #
        # self.update()
        # if serializer.is_valid():
        #     print("dddddddddddddddddddddddddd")
        #     print(serializer.validated_data)
        #     serializer.save(chatRoomMember_name=chatroommember_serializer)
        #
        # self.perform_create(serializer)
        #
        # print(serializer)
        # self.perform_update(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override
    # url에 입력한 group_id에 해당하는 ChatRoom query set을 반환
    def get_queryset(self):
        group_id = self.kwargs['group_id']  # data in url
        print("group_id:" + str(group_id))

        return ChatRoom.objects.filter(group_id=group_id)

    # override
    # url에 입력한 group_id에 해당하는 ChatRoom 생성
    # TODO (front: 초기 생성자 이름으로 방 이름을 세팅)
    # TODO 채팅방 초대 기능 추가
    def perform_create(self, serializer):
        group_id = self.kwargs['group_id']  # data in url
        print("group_id: " + str(group_id))
        group = Group.objects.get(pk=group_id)

        serializer.save(group=group)

    def perform_update(self, serializer):
        instance = serializer.save()
        # chatRoom_id = serializer.data['id']
        print(serializer.data)  # ChatRoomListSerializer
        chatRoomMember = ChatRoomMember.objects.all()
        print(chatRoomMember)

        print("chatRoom_id: " + str(serializer.data['id']))
        chatRoom = ChatRoom.objects.get(pk=serializer.data['id'])

        print(chatRoom.chatRoomMembers)

        serializer.save() #??


class ChatRoomDetailViewSet(ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomDetailSerializer

    # detail [GET] 채팅방 안의 내용 및 파일정보 가져오기
    def retrieve(self, request, *args, **kwargs):
        """
        Room view - show the topic, with latest topicmessages.
        The template for this view has the WebSocket business to send and stream message,
        so see the template for wherer the magic happens.
        """
        # If the room with the given topic_id doesn't exist, automatically create it
        # upon first visit
        chatroom_id = self.kwargs['chatroom_id']
        print("chatroom_id: " + str(chatroom_id))

        chatroom, created = ChatRoom.objects.get_or_create(pk=chatroom_id)
        chatroom_serializer = ChatRoomDetailSerializer(chatroom)

        chatroom_message = chatroom.chatRoomMessages.order_by('-created_time')[:50]
        chatroom_message_serializer = ChatRoomMessageSerializer(chatroom_message, many=True)

        # We want to show the last 50 messages, ordered most-recent-last
        # topic_message = reversed(topic_message_serializer)

        # url에 입력한 chatroom_id에 해당하는 Chatroom Serializer와 해당 chatroom의 기존 message들을 가져온다
        response_json_data = {
            'chatroom_serializer': chatroom_serializer.data,
            'chatroom_message_serializer': chatroom_message_serializer.data,
        }

        return Response(response_json_data)

    # detail [DELETE] 채팅방 삭제(기본 토픽은 삭제 불가)
    # TODO ChatRoomMember에서 제거
    def destroy(self, request, *args, **kwargs):
        chatroom_id = self.kwargs['chatroom_id']
        chatroom = self.get_object(chatroom_id)
        chatroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # override
    # pk에 해당하는 ChatRoom obj를 반환
    def get_object(self, pk):
        try:
            return ChatRoom.objects.get(pk=pk)
        except ChatRoom.DoesNotExist:
            raise Http404  ### TODO error 수정 필요

    # override
    # url에 입력한 chatroom_id에 해당하는 ChatRoom query set을 반환
    def get_queryset(self):
        chatroom_id = self.kwargs['chatroom_id']  # data in url
        print("chatroom_id:" + str(chatroom_id))

        return ChatRoom.objects.get(pk__in=chatroom_id)

##########################################################################


class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, format=None):
        print("ddddddddddd")
        print(request)
        filename = self.request.data['filename']
        print(str(filename))
        file_obj = request.FILES['file']
        # do some stuff with uploaded file
        return Response(status=204)