from channels.db import database_sync_to_async

from .exceptions import ClientError
from .models import Topic, TopicMessage
from .serializers import TopicMessageSerializer


# This decorator turns this function from a synchronous function into an async one
# we can call from our async consumers, that handles Django DBs correctly.
# For more, see http://channels.readthedocs.io/en/latest/topics/databases.html
@database_sync_to_async
def get_room_or_error(room_id, user, room_type):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    # if not user.is_authenticated:
    #     raise ClientError("USER_HAS_TO_LOGIN")
    # Find the room they requested (by ID)
    try:
        if room_type == "topics":
            room = Topic.objects.get(pk=room_id)
        elif room_type == "chats":
            # room = Chat.objects.get(pk=room_id)
            pass
    except Topic.DoesNotExist:
        raise ClientError("Topic ROOM_INVALID")
    # except Chat.DoesNotExist:
    #     raise ClientError("Chat ROOM_INVALID")

    # Check permissions
    # if room.staff_only and not user.is_staff:
    #     raise ClientError("ROOM_ACCESS_DENIED")
    return room


@database_sync_to_async
def get_previous_messages(room_id, user, room_type):
    try:
        if room_type == "topics":
            room = Topic.objects.get(pk=room_id)
            # We want to show the last 100 messages, ordered most-recent-last
            # (기존의 메시지 100개를 가져온다)
            queryset = TopicMessage.objects.filter(topic_id=room.id)
            qs = queryset.order_by("-created_time")[:100]
            print("qs count: " + str(qs.count()))

            messages_serializer = TopicMessageSerializer(qs, many=True)

            response_json_data = {
                'messages_serializer': messages_serializer.data,
            }
            print(response_json_data)

        elif room_type == "chats":
            # room = Chat.objects.get(pk=room_id)
            pass
    except Topic.DoesNotExist:
        raise ClientError("Topic ROOM_INVALID")
    # except Chat.DoesNotExist:
    #     raise ClientError("Chat ROOM_INVALID")

    # Check permissions
    # if room.staff_only and not user.is_staff:
    #     raise ClientError("ROOM_ACCESS_DENIED")
    return response_json_data
