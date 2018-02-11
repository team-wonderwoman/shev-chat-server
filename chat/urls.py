from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    GroupListAPIView,
    GroupInviteAPIView,
    # TopicListAPIView,
    # TopicDetailAPIView,

    TopicListViewSet,
    TopicDetailViewSet
)

topic_list = TopicListViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

topic_detail = TopicDetailViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    # 'patch': 'partial_update',
    'delete': 'destroy'
})

# API endpoints
urlpatterns = format_suffix_patterns([
    # api/group/:user_id
    # 사용자의 그룹 리스트를 보여준다
    url(r'^(?P<user_id>\d+)/$', GroupListAPIView.as_view(), name='group_list'),

    # api/group/:group_id/topics [GET][POST]
    url(r'^(?P<group_id>\d+)/topics/$', topic_list, name='topic_list'),

    # api/group/:group_id/topics/:topic_id [GET][PUT][DELETE]
    url(r'^(?P<group_id>\d+)/topics/(?P<topic_id>\d+)$', topic_detail, name='topic_detail'),

    # # api/group/:group_id/topics [GET][POST]
    # url(r'^(?P<group_id>\d+)/topics/$', TopicListAPIView.as_view(), name='topic_list'),
    #
    # # api/group/:group_id/topics/:topic_id [GET][PUT][DELETE]
    # url(r'^(?P<group_id>\d+)/topics/(?P<topic_id>\d+)$', TopicDetailAPIView.as_view(), name='topic_detail'),
    url(r'^(?P<user_id>\d+)/invitation/$',GroupInviteAPIView.as_view(), name='group_invite'),

    url(r'^join/(?P<uid64>[0-9A-Za-z_\-]+)/(?P<verify_token>[0-9A-Za-z]+)/$',
        GroupInviteAPIView.as_view(), name='group_join'),
])
