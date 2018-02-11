import json
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models import Group, GroupMember, Topic
from AuthSer.models import User

from .serializers import (
    GroupListSerializer,
    GroupMemberModelSerializer,
    TopicListSerializer,
    TopicDetailSerializer,
)
from common.const import const_value, status_code
from .sendmail import send_verification_mail, send_registration_mail ,decode_verify_token
from AuthSer.redis import redis_exists, redis_get


# 로그인한 사용자의 GroupMember List 를 반환
# @method_decorator(login_required, name='dispatch')
class GroupListAPIView(ListAPIView):
    serializer_class = GroupListSerializer

    def get(self, *args, **kwargs):
        queryset = self.get_queryset()
        qs = Group.objects.all()
        for i in qs:
            print(i.id, end=' , ')
            print(i.group_name, end=' , ')
            print(i.members, end=' , ')
            print(i.manager_id.id)
        user_id = int(self.kwargs['user_id'])  # url에 있는 user_id를 가져온다
        print(user_id)

        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)  # user가 속한 group을 가져온다
            print("user_id is Not None")
            for i in queryset:
                print(i.id, end=' , ')
                print(i.group_id.id, end=' , ')
                print(i.user_id.id, end=' , ')
                print(i.is_active)
            qs = qs.filter(pk=queryset.group_id)  # 해당 group의 name을 가져온다
            serializer = GroupListSerializer(qs)
            print(serializer.data)
            return Response(serializer.data)


    # override
    def get_queryset(self, *args, **kwargs):
        queryset = GroupMember.objects.all()
        print("GroupMemberModelSerializer")
        for i in queryset:
            print(i.id,end=' , ')
            print(i.group_id.id,end=' , ')
            print(i.user_id.id, end=' , ')
            print(i.is_active)
        #print(queryset)
        return queryset

    # group [POST] 새로운 그룹 생성
    def post(self, request , *args, **kwargs):
        userId = self.kwargs['user_id']

        # 그룹 이름
        group_name = request.data['group_name']

        # 그룹 생성자 (현재 User의 pk)
        request.data['manager_id'] = userId

        print(request.data)

        serializer = GroupListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'result' : status_code['GROUP_MADE_SUCCESS'], 'received_data' : serializer.data} , status=status.HTTP_200_OK)
        else:
            return Response({'result': status_code['GROUP_MADE_FAILURE'], 'received_data' : request.data}, status = status.HTTP_200_OK)


# 그룹 초대 및 이메일 인증 활성화 처리
class GroupInviteAPIView(ListAPIView):
    # [GET] 이메일 인증 처리
    def get(self, request, *args, **kwargs):
        print("invite인증처리들어와?")

        uid = force_text(urlsafe_base64_decode(self.kwargs['uid64']))
        verify_token = force_text(urlsafe_base64_decode(self.kwargs['verify_token']))

        print('Group_inviteAPIView_uid : %s, verify_token : %s' % (uid,verify_token))

        uid = int(uid)
        try:
            print("query 날리기 전")
            query = User.objects.get(id=uid)

        except query is None:
            print("invite activate 안됨!!")
            return Response({'result': status_code['GROUP_INVITATION_ACTIVATE_FAILURE'], 'received_data' : request.data, 'query' : query}, status = status.HTTP_200_OK)

        # if redis_get(verify_token) == str(uid):
        #     verify_token = jwt.decode(verify_token)
        #     print("verify-[toekn redis get?")
        #     print(verify_token)

        verify_token = decode_verify_token(verify_token)
        print(verify_token)

        group = Group.objects.get(group_name=verify_token)
        print("group_id??", end='')
        print(group.id)

        dict = ({"group_id" : group.id , "user_id" : uid , "is_active" : True})
        print("json_dumps 전 dict ", end='')
        print(type(dict))

        dict = json.dumps(dict)

        print(type(dict))

        dict_dump = json.loads(dict)
        print("json_loads 후 dict ", end='')
        print(dict_dump)
        print(type(dict_dump))

        print("????")
        serializer = GroupMemberModelSerializer(data=dict_dump)
        print("?>DJKLSDF?")

        if serializer.is_valid(raise_exception=True):
            print("verify_token_invitation_들어와따!")
            serializer.save()
            print(serializer.data['group_id'])
            print(serializer.data['user_id'])
            print(serializer.data['is_active'])
            return Response({'result': status_code['GROUP_INVITATION_ACTIVATE_SUCCESS'], 'saved_data' : serializer.data}, status = status.HTTP_200_OK)
        return Response({'result' : status_code['GROUP_INVITATION_ACTIVATE_FAILURE'] , 'received_data' : request.data} , status=status.HTTP_200_OK)

    # [POST] 그룹에 멤버 초대
    def post(self, request, *args, **kwargs):
        userId = self.kwargs['user_id']

        # 그룹 이름
        group_name = request.data['group_name']
        # 그룹 참여자의 이메일
        participants = request.data['members']

        # 그룹 생성자 (현재 User의 pk)
        request.data['manager_id'] = int(userId)

        # DB에서 그룹 참여자 pk 가져오기
        try:
            queryset = User.objects.get(user_email=participants)
            qs = Group.objects.get(group_name=group_name)
            print("qs는?")
            print(qs.id)
            request.data['group_id'] = qs.id
            request.data['user_id'] = queryset.id
            request.data['is_active'] = False

        except queryset is None:
            return Response({'result': status_code['GROUP_INVITATION_FAILURE'], 'result' : request.data}, status=status.HTTP_200_OK)

        print(request.data)

        # 이메일보내기
        send_verification_mail(group_name, participants, queryset)

        print("이메일 보내기 완료")

        serializer = GroupMemberModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'result': status_code['GROUP_INVITATION_SUCCESS'], 'received_data': serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'result': status_code['GROUP_INVITATION_FAILURE'], 'received_data': request.data},
                            status=status.HTTP_200_OK)


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

