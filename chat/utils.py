from channels.db import database_sync_to_async

from .exceptions import ClientError
from .models import Topic, TopicMessage, ChatRoom, ChatRoomMessage
from .serializers import TopicMessageSerializer, ChatRoomMessageSerializer
from AuthSer.models import User

# This decorator turns this function from a synchronous function into an async one
# we can call from our async consumers, that handles Django DBs correctly.
# For more, see http://channels.readthedocs.io/en/latest/topics/databases.html
@database_sync_to_async
def get_room_or_error(room_id, user, room_type):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    room = None

    try:
        if room_type == "topics" or room_type == None:
            room = Topic.objects.get(pk=room_id)
        elif room_type == "chatrooms":
            room = ChatRoom.objects.get(pk=room_id)
            pass
    except Topic.DoesNotExist:
        raise ClientError("Topic ROOM_INVALID")
    except ChatRoom.DoesNotExist:
        raise ClientError("Chat ROOM_INVALID")

    # Check permissions
    # if room.staff_only and not user.is_staff:
    #     raise ClientError("ROOM_ACCESS_DENIED")

    return room


@database_sync_to_async
def get_previous_messages(room_id, user, room_type):
    response_json_data = None

    try:
        if room_type == "topics":
            room = Topic.objects.get(pk=room_id)
            # We want to show the last 100 messages, ordered most-recent-last
            # (기존의 메시지 50개를 가져온다)
            queryset = TopicMessage.objects.filter(topic_id=room.id)
            qs = queryset.order_by("pk")[:50]
            print("qs count: " + str(qs.count()))

            messages_serializer = TopicMessageSerializer(qs, many=True)
            response_json_data = {
                'messages_serializer': messages_serializer.data,
            }
            print("[[get_previous_messages]] topics")
            print(response_json_data)
        elif room_type == "chatrooms":
            room = ChatRoom.objects.get(pk=room_id)
            # We want to show the last 100 messages, ordered most-recent-last
            # (기존의 메시지 50개를 가져온다)
            queryset = ChatRoomMessage.objects.filter(chatRoom=room.id)
            qs = queryset.order_by("pk")[:50]
            print("qs count: " + str(qs.count()))

            messages_serializer = ChatRoomMessageSerializer(qs, many=True)

            response_json_data = {
                'messages_serializer': messages_serializer.data,
            }
            print("[[get_previous_messages]] chatrooms")
            print(response_json_data)
            pass
        else:
            response_json_data = {
                'messages_serializer': [],
            }
            print("[[get_previous_messages]] None")
            print(response_json_data)

    except Topic.DoesNotExist:
        raise ClientError("Topic ROOM_INVALID")
    except ChatRoom.DoesNotExist:
        raise ClientError("Chat ROOM_INVALID")

    # Check permissions
    # if room.staff_only and not user.is_staff:
    #     raise ClientError("ROOM_ACCESS_DENIED")
    return response_json_data


# 스크롤을 올리면 가장 최신의 messages 50개를 반환한다


# 받은 message를 Redis/DB에 저장한다
@database_sync_to_async
def save_message(room_id, sender_id, room_type, message):
    room = None
    print("[[save_message]]")
    sender = User.objects.get(pk=sender_id)

    try:
        if room_type == "topics":
            room = Topic.objects.get(pk=room_id)
            topicMessage = TopicMessage.objects.create(user_id=sender, topic_id=room, contents=message)
            print(topicMessage)
        elif room_type == "chatrooms":
            room = ChatRoom.objects.get(pk=room_id)
            chatRoomMessage = ChatRoomMessage.objects.create(user=sender, chatRoom=room, contents=message)
            print(chatRoomMessage)
            pass
        else:
            print("[[save_message]] error")
    except Topic.DoesNotExist:
        raise ClientError("Topic ROOM_INVALID")
    except ChatRoom.DoesNotExist:
        raise ClientError("Chat ROOM_INVALID")

    return sender.user_name
