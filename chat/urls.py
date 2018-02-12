from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    GroupListAPIView,
    GroupDetailAPIView,

    # TopicListAPIView,
    # TopicDetailAPIView,

    TopicListViewSet,
    TopicDetailViewSet,

    FileUploadView
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

    # api/group/:user_id/:group_id
    # 사용자 그룹의 Topic과 Chat list를 반환한다
    url(r'^(?P<user_id>\d+)/(?P<group_id>\d+)/$', GroupDetailAPIView.as_view(), name='group_detail'),

    # api/group/:group_id/topics [GET][POST]
    url(r'^(?P<group_id>\d+)/topics/$', topic_list, name='topic_list'),

    # api/group/:group_id/topics/:topic_id [GET][PUT][DELETE]
    url(r'^(?P<group_id>\d+)/topics/(?P<topic_id>\d+)/$', topic_detail, name='topic_detail'),

    # api/group/fileupload
    url(r'^fileupload/$', FileUploadView.as_view())
    # url(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view())

    # # api/group/:group_id/topics [GET][POST]
    # url(r'^(?P<group_id>\d+)/topics/$', TopicListAPIView.as_view(), name='topic_list'),
    #
    # # api/group/:group_id/topics/:topic_id [GET][PUT][DELETE]
    # url(r'^(?P<group_id>\d+)/topics/(?P<topic_id>\d+)$', TopicDetailAPIView.as_view(), name='topic_detail'),
])
