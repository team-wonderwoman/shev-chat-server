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

from .models import Group, GroupMember, Topic
from shevauthserver.models import User

from .serializers import (
    GroupListSerializer,
    TopicListSerializer,
    TopicDetailSerializer,
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
    rooms = Topic.objects.filter(group_id=2).order_by("group_id")
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
        queryset = self.get_queryset()
        qs = Group.objects.all()
        user_id = self.kwargs['user_id']  # url에 있는 user_id를 가져온다
        print(user_id)

        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)  # user가 속한 group을 가져온다
            qs = qs.filter(pk__in=queryset.values('group_id'))  # 해당 group의 name을 가져온다
            serializer = GroupListSerializer(qs)
            print(serializer.data)
            return Response(serializer.data)

    # override
    def get_queryset(self, *args, **kwargs):
        queryset = GroupMember.objects.all()

        return queryset


##########################################################################

class TopicListViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicListSerializer

    # list [GET] 해당 그룹의 토픽 리스트 조회
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = TopicListSerializer(queryset, many=True)  # 해당 group의 모든 topic_name을 가져온다
        return Response(serializer.data)

    # list [POST] 해당 그룹의 토픽 생성
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
        # We want to show the last 100 messages, ordered most-recent-last
        topic_message = reversed(topic.topic_messages.order_by('-created_time')[:100])

        # url에 입력한 topic_id에 해당하는 Topic Serializer와 해당 topic의 기존 message들을 가져온다
        response_json_data = {
            # 'topic': topic,
            'topic_serializer': topic_serializer.data,
            'topic_message': topic_message
        }
        print(response_json_data)

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