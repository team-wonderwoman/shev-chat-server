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
        group_id = self.kwargs['group_id']
        print(group_id)

        return Topic.objects.filter(group_id=group_id)

    # override
    # url에 입력한 group_id에 해당하는 Topic에 POST로 넘어온 topic_name을 세팅 후 save
    def perform_create(self, serializer):
        topic_name = self.request.data['topic_name']
        print(topic_name)

        group_id = self.kwargs['group_id']
        group = Group.objects.get(pk=group_id)

        serializer.save(group_id=group, topic_name=topic_name)


class TopicDetailViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicDetailSerializer

    # detail [GET] 토픽 안의 내용 및 파일정보 가져오기
    def retrieve(self, request, *args, **kwargs):
        return Response

    # detail [PUT] 토픽 이름 변경
    def update(self, request, *args, **kwargs):
        return Response

    # detail [DELETE] 토픽 삭제(기본 토픽은 삭제 불가)
    def destroy(self, request, *args, **kwargs):
        return Response


# class TopicListAPIView(ListCreateAPIView):
#     queryset = Topic.objects.all()
#
#     # 해당 그룹의 토픽 리스트 조회
#     def get(self):
#         return Response
#
#     # 해당 그룹의 토픽 생성
#     def post(self, request, *args, **kwargs):
#         return Response
#
#
# class TopicDetailAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Topic.objects.all()
#     serializer_class = TopicDetailSerializer
#
#     # 토픽 안의 내용 및 파일정보 가져오기
#     def get(self):
#         return Response
#
#     # 토픽 이름 변경
#     def put(self, request, *args, **kwargs):
#         return Response
#
#     # 토픽 삭제기본 토픽은 삭제 불가)
#     def delete(self, request, *args, **kwargs):
#         return Response


##########################################################################

