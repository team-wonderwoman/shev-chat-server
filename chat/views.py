import json
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

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from .models import Group, GroupMember, Topic
from AuthSer.models import User

from .serializers import (
    GroupListSerializer,
    GroupMemberModelSerializer,
    TopicListSerializer,
    TopicDetailSerializer,
    TopicMessageSerializer,
)

from common.const import const_value, status_code
from .sendmail import send_verification_mail, decode_verify_token

## for file
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView

from AuthSer.serializers import UserModelSerializer

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

    # [GET] User가 속한 그룹 조회 (그룹 이름만)
    def get(self, *args, **kwargs):
        queryset = self.get_queryset() # GroupMember 에서 사용자와 그룹 간 관계 가져옴
        qs = Group.objects.all() # 존재하는 그룹을 모두 가져옴
        user_id = int(self.kwargs['user_id'])  # url에 있는 user_id를 가져옴
        print(user_id)

        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)  # user가 속한 group의 group_id 만을 가져옴
            qs = qs.filter(pk__in=queryset.values('group_id'))  # 해당 group의 group_id로 group_name을 가져옴
            serializer = GroupListSerializer(qs, many=True)
            #manager = User.objects.filter(pk__in=qs.values('manager_id'))

            #dict = convert_query_to_dict(qs, manager)
            print(serializer.data)
            status_code['GROUP_LIST_SUCCESS']['data'] = serializer.data
            return Response({
                'result' : status_code['GROUP_LIST_SUCCESS']}, status=status.HTTP_200_OK)
        else:
            return Response({'result' : status_code['GROUP_LIST_FAILURE']}, status=status.HTTP_200_OK)


    # override [GET] GroupMember 테이블의 모든 컬럼 조회
    def get_queryset(self, *args, **kwargs):
        queryset = GroupMember.objects.all()
        return queryset

    # group [POST] 새로운 그룹 생성
    def post(self, request , *args, **kwargs):
        userId = int(self.kwargs['user_id']) # url에 있는 user_id를 가져옴

        # manager_id를 현재 User의 pk로 지정 (그룹 생성자)
        request.data['manager_id'] = userId

        # Group 모델에 request.data 저장
        serializer = GroupListSerializer(data=request.data)
        try :
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print("GroupListAPIView - GroupMember serializer")
            print(serializer.data['id'])
            groupId = serializer.data['id'] # 현재 그룹의 pk 가져옴
            member_query = User.objects.get(pk=userId) # 현재 사용자에 대한 정보 가져옴

            #group_query = GroupMember.objects.filter(pk=groupId)
            #print(group_query)
        except:
            status_code['GROUP_MADE_FAILURE']['data'] = request.data
            return Response({'result': status_code['GROUP_MADE_FAILURE']}, status = status.HTTP_200_OK)


        request.data['group_id'] = groupId # request.data에 group_id 세팅 (사용자가 생성한 그룹의 pk)
        request.data['user_id'] = userId # request.data에 user_id 세팅 (사용자의 pk)
        request.data['is_active'] = True # request.data에 is_active 세팅 (그룹의 생성자여서 인증할 필요 없으므로 True)

        print("serializer_member")
        print(request.data)

        try : #  GroupMember 테이블에 request.data 저장
            serializer_member = GroupMemberModelSerializer(data=request.data)
            serializer_member.is_valid(raise_exception=True)

            print("serializer_member valid??")
            serializer_member.save()

            print(serializer_member.data)
            print("save됨")

            status_code['GROUP_MADE_SUCCESS']['data'] = serializer_member.data
            return Response({'result': status_code['GROUP_MADE_SUCCESS']},
                            status=status.HTTP_200_OK)
        except :
            return Response({'result': status_code['GROUP_MADE_FAILURE'], 'data' : serializer.data,'received_data': request.data},
                            status=status.HTTP_200_OK)


#TEST
# 그룹 내 멤버 조회
class GroupMemberAPIView(APIView):
    # [GET] 그룹 내 멤버 조회
    def get(self, request, *args, **kwargs):
        groupId = self.kwargs['group_id'] # 조회 할 그룹의 id를 url로부터 가져옴
        queryset = self.get_user_queryset() # User 테이블의 모든 정보 가져옴
        member_query = GroupMember.objects.filter(group_id=groupId) # 사용자가 속한 그룹의 그룹 멤버들을 가져옴

        if groupId is not None:
            queryset = queryset.filter(pk__in=member_query.values('user_id')) # 사용자가 속한 그룹의 멤버들의 id로 User object 가져옴
            serializer = UserModelSerializer(queryset, many=True)
            print(serializer.data)

            status_code['GROUP_MEMBER_GET_SUCCESS']['data'] = serializer.data
            return Response({'result' : status_code['GROUP_MEMBER_GET_SUCCESS']}, status=status.HTTP_200_OK)

        return Response({'result': status_code['GROUP_MEMBER_GET_FAILURE']}, status=status.HTTP_200_OK)

    # User 테이블의 모든 정보를 가져오기 위한 함수
    def get_user_queryset(self, *args, **kwargs):
        queryset = User.objects.all()
        return queryset

# 그룹에 멤버 초대 - 이메일 보내기
class GroupInviteAPIView(APIView):
    # [GET] 모든 그룹 조회
    def get(self, request, *args, **kwargs):
        qs = Group.objects.all()
        status_code['SUCCESS']['data'] = qs.values()
        return Response({'result' : status_code['SUCCESS']}, status=status.HTTP_200_OK)

    # [POST] 그룹에 멤버 초대
    def post(self, request, *args, **kwargs):
        userId = self.kwargs['user_id']
        print(request.data['group_id'])
        # 그룹 이름
        groupId = request.data['group_id']
        # 그룹 참여자의 이메일
        participants = request.data['members']

        # 그룹 생성자 (현재 User의 pk)
        request.data['manager_id'] = int(userId)

        # DB에서 그룹 참여자 pk 가져오기
        try:
            queryset = User.objects.get(user_email=participants)
            #qs = Group.objects.get(pk=groupId)
            # print("qs는?")
            # print(qs.id)
            #group_name = qs.group_name
            print("qs.group_id", end=' ')
            print(groupId)

            request.data['user_id'] = queryset.id
            request.data['is_active'] = False

        except queryset is None:
            status_code['GROUP_INVITATION_FAILURE']['data'] = request.data
            return Response({'result': status_code['GROUP_INVITATION_FAILURE']}, status=status.HTTP_200_OK)


        # 이메일보내기
        send_verification_mail(groupId, participants, queryset)

        print("이메일 보내기 완료")

        serializer = GroupMemberModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            status_code['GROUP_INVITATION_SUCCESS']['data'] = serializer.data
            return Response({'result': status_code['GROUP_INVITATION_SUCCESS']},
                            status=status.HTTP_200_OK)
        else:
            status_code['GROUP_INVITATION_ACTIVATE_FAILURE']['data'] = request.data
            return Response({'result': status_code['GROUP_INVITATION_FAILURE']},
                            status=status.HTTP_200_OK)

# 그룹 초대 메일 인증 처리
class GroupJoinAPIView(APIView):

    # [GET] 이메일 인증 처리 - 사용자가 메일로 발송된 url 클릭 시 is_activate 필드 True로 바꿈
    def get(self, request, *args, **kwargs):
        uid = force_text(urlsafe_base64_decode(self.kwargs['uid64']))  # url에 있는 base64 인코딩 된 uid를 decode해서 가져옴
        verify_token = force_text(urlsafe_base64_decode(self.kwargs['verify_token'])) # url에 있는 token을 decode해서 가져옴

        print('Group_inviteAPIView_uid : %s, verify_token : %s' % (uid, verify_token))

        uid = int(uid)
        try:
            # TODO query 지우기
            query = User.objects.get(id=uid) # 인증할 사용자의 data를 가져옴

        except query is None:
            return Response({'result': status_code['GROUP_INVITATION_ACTIVATE_FAILURE']}, status=status.HTTP_200_OK)

        verify_token = decode_verify_token(verify_token) # 그룹 초대 인증 토큰 확인 - 그룹 아이디 꺼내옴

        group = Group.objects.get(pk=verify_token)

        print("group_id??", end='')
        print(group)


        try:
            group_active_qs = GroupMember.objects.filter(group_id=group.id, user_id=uid)
            group_active_qs.update(is_active=True)
            status_code['GROUP_INVITATION_ACTIVATE_SUCCESS']['data'] = group_active_qs.values()
            return Response(
                {'result': status_code['GROUP_INVITATION_ACTIVATE_SUCCESS']},
                status=status.HTTP_200_OK)

        except group_active_qs is None:
            status_code['GROUP_INVITATION_ACTIVATE_FAILURE']['data'] = group_active_qs.values()
            return Response({'result': status_code['GROUP_INVITATION_ACTIVATE_FAILURE']},status=status.HTTP_200_OK)

class GroupDetailAPIView(APIView):

    # [GET] user가 속한 그룹의 Topic, Chat list를 반환한다
    def get(self, *args, **kwargs):
        print("groupdetailapiview")
        group_id = self.kwargs['group_id']
        queryset = Topic.objects.filter(group_id=group_id).order_by('pk')
        serializer = TopicListSerializer(queryset, many=True)
        return Response(serializer.data)

# 그룹 삭제
class GroupDeleteAPIView(ListAPIView):

    # [POST] 현재 그룹 삭제
    def delete(self,request, *args, **kwargs):
        userId = int(self.kwargs['user_id'])
        groupId = int(self.kwargs['group_id'])
        print("userId " + str(userId) + " groupId " + str(groupId))

        manager_query = Group.objects.get(pk=groupId)


        print("manager_query.manager_id.id", end=' ')
        print(manager_query.manager_id.id, end= ' : ')
        print(type(manager_query.manager_id_id))
        print("userId", end=' ')
        print(userId, end=' : ')
        print(type(userId))

        if manager_query.manager_id.id == userId : # 현재 사용자가 그룹 관리자인 경우 - 그룹 자체를 삭제
            to_delete = get_object_or_404(Group, pk=groupId)
            to_delete.delete()
            #manager_query.delete()
            print("지움")
            status_code['GROUP_EXIT_SUCCESS']['msg'] += "\n You are manager of this group."
            #status_code['GROUP_EXIT_SUCCESS']['data'] = user_query.values()
            return Response({'result' : status_code['GROUP_EXIT_SUCCESS']}, status=status.HTTP_200_OK)

        else: # 현재 사용자가 그룹 관리자가 아닌 경우 - 그룹 삭제 불가
            status_code['GROUP_EXIT_FAIL']['msg'] += "\n You are not a manager of this group."
            #status_code['GROUP_EXIT_FAIL']['data'] = user_query.values()
            return Response({'result': status_code['GROUP_EXIT_FAIL']}, status=status.HTTP_200_OK)

# 그룹 나가기
class GroupExitAPIView(ListAPIView):

    # [POST] 현재 그룹 나가기
    def delete(self,request, *args, **kwargs):
        userId = int(self.kwargs['user_id'])
        groupId = int(self.kwargs['group_id'])
        print("userId " + str(userId) + " groupId " + str(groupId))

        manager_query = Group.objects.get(pk=groupId)

        if manager_query.manager_id.id != userId : # 현재 사용자가 그룹 관리자가 아닌 경우 - 그룹 나가기 가능
            group_relation = get_object_or_404(GroupMember, group_id=groupId,user_id=userId)
            group_relation.delete()
            status_code['GROUP_LIST_SUCCESS']['data'] = manager_query.values()
            return Response({'result': status_code['GROUP_EXIT_SUCCESS']}, status=status.HTTP_200_OK)

        else: # 현재 사용자가 그룹 관리자인 경우 - 그룹 나가기 불가능
            status_code['GROUP_EXIT_FAIL']['msg'] += "\n You are not a manager of this group."
            status_code['GROUP_EXIT_FAIL']['data'] = manager_query.values()
            return Response({'result': status_code['GROUP_EXIT_FAIL']}, status=status.HTTP_200_OK)




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

        topic_message = topic.topic_messages.order_by('-created_time')[:100]
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