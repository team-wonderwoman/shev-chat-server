import json
import logging
from channels import Channel, Group
from channels.sessions import channel_session
from channels.auth import channel_session_user_from_http, channel_session_user
from .settings import MSG_TYPE_LEAVE, MSG_TYPE_ENTER, NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS
# from .models import ChatRoom
from .models import Topic
from .utils import get_room_or_error, catch_client_error
from .exceptions import ClientError

log = logging.getLogger(__name__)


# -- WebSocket handling --


# This decorator copies the user from the HTTP session (only available in
# websocket.connect or http.request messages) to the channel session (available
# in all consumers with the same reply_channel, so all three here)
@channel_session_user_from_http
def ws_connect(message):
    message_path_list = message['path'].strip('/').split('/')
    message_client_list = message['client']
    print("---message path: " + str(message['path']))
    print("---message path list: " + str(message_path_list))
    print("---message client: ", message_client_list[0], message_client_list[1])

    group_id = message_path_list[2]
    check_roomtype = message_path_list[3]
    room_id = message_path_list[-1]

    if check_roomtype == "topics":
        print("**about topics**")
        room = Topic.objects.get(pk=room_id)
        message.reply_channel.send({'accept': True})
        Group(
            # 'chat-' + topic_or_chatroom_id,
            'chat-' + room.topic_name,
            channel_layer=message.channel_layer
        ).add(message.reply_channel)

    elif check_roomtype == "chats":
        print("about chats")
        pass

    # Initialise their session
    # 해당 topic으로 session을 초기화한다
    message.channel_session['rooms'] = room.topic_name  # ???


# Unpacks the JSON in the received WebSocket frame and puts it onto a channel
# of its own with a few attributes extra so we can route it
# This doesn't need @channel_session_user as the next consumer will have that,
# and we preserve message.reply_channel (which that's based on)
@channel_session
def ws_receive(message):
    # All WebSocket frames have either a text or binary payload; we decode the
    # text part here assuming it's JSON.
    # You could easily build up a basic framework that did this encoding/decoding
    # for you as well as handling common errors.

    # payload = json.loads(message['text'])
    # payload['reply_channel'] = message.content['reply_channel']
    # Channel("chat.receive").send(payload)

    print("tttttttttttttttttttttt")

    try:
        topic_or_chatroom_id = message.channel_session['room']
        room = Topic.objects.get(pk=topic_or_chatroom_id)
        print(room.topic_name)
    except KeyError:
        print("KeyError")
        return
    except Topic.DoesNotExist:
        print("recieved message, buy room does not exist topic: ", topic_or_chatroom_id)
        return

    try:
        data = json.loads(message['text'])
    except ValueError:
        print("ValueError")
        return

    if set(data.keys()) != set(('message')):
        print(data)
        return

    if data:
        print(data['message'])
        m = room.topic_messages.create(**data)

        Group(
            # 'chat-'+topic_or_chatroom_id,
            'chat-' + room.topic_name,
            channel_layer=message.channel_layer
        ).send({'text': json.dumps(m.as_dict())})


@channel_session_user
def ws_disconnect(message):
    # Unsubscribe from any connected rooms
    # for room_id in message.channel_session.get("rooms", set()):
    #     try:
    #         room = Topic.objects.get(pk=room_id)
    #         # Removes us from the room's send group. If this doesn't get run,
    #         # we'll get removed once our first reply message expires.
    #         room.websocket_group.discard(message.reply_channel)
    #     except Topic.DoesNotExist:
    #         pass
    try:
        topic_or_chatroom_id = message.channel_session['room']
        room = Topic.objects.get(pk=topic_or_chatroom_id)
        Group(
            # 'chat-'+topic_or_chatroom_id,
            'chat-' + room.topic_name,
            channel_layer=message.channel_layer
        ).discard(message.reply_channel)
    except (KeyError, Topic.DoesNotExist):
        pass

##############################################################################################

# -- Chat channel handling --


# Channel_session_user loads the user out from the channel session and presents
# it as message.user. There's also a http_session_user if you want to do this on
# a low-level HTTP handler, or just channel_session if all you want is the
# message.channel_session object without the auth fetching overhead.
@channel_session_user
@catch_client_error
def chat_join(message):
    # Find the room they requested (by ID) and add ourselves to the send group
    # Note that, because of channel_session_user, we have a message.user
    # object that works just like request.user would. Security!
    print("chat_join(room_id): " + str(message["room"]))
    room = get_room_or_error(message["room"], message.user)  # room_id에 맞는 Topic을 반환

    # Send a "enter message" to the room if available
    # room_id, message, username, msg_type를 client에 넘겨준다
    if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        room.send_message(None, message.user, MSG_TYPE_ENTER)

    # OK, add them in. The websocket_group is what we'll send messages
    # to so that everyone in the chat room gets them.
    # ws_connect에서 만든 session에 join
    room.websocket_group.add(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).union([room.id]))
    # Send a message back that will prompt them to open the room
    # Done server-side so that we could, for example, make people
    # join rooms automatically.

    # client의 data에 넘겨주는 json data
    # 이 메시지에 따라 client에서 다음 상황을 처리...
    message.reply_channel.send({
        "text": json.dumps({
            "join": str(room.id),
            "title": room.title,
        }),
    })


@channel_session_user
@catch_client_error
def chat_leave(message):
    # Reverse of join - remove them from everything.
    room = get_room_or_error(message["room"], message.user)

    # Send a "leave message" to the room if available
    if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        room.send_message(None, message.user, MSG_TYPE_LEAVE)

    room.websocket_group.discard(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).difference([room.id]))
    # Send a message back that will prompt them to close the room
    message.reply_channel.send({
        "text": json.dumps({
            "leave": str(room.id),
        }),
    })


@channel_session_user
@catch_client_error
def chat_send(message):
    # Check that the user in the room
    if int(message['room']) not in message.channel_session['rooms']:
        raise ClientError("ROOM_ACCESS_DENIED")
    # Find the room they're sending to, check perms
    room = get_room_or_error(message["room"], message.user)
    # Send the message along
    room.send_message(message["message"], message.user)
