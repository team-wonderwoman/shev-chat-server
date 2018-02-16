from django.conf import settings

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .exceptions import ClientError
from .utils import get_room_or_error, get_previous_messages, save_message
from .models import Topic, TopicMessage


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    This chat consumer handles websocket connections for chat clients.

    It uses AsyncJsonWebsocketConsumer, which means all the handling functions
    must be async functions, and any sync work (like ORM access) has to be
    behind database_sync_to_async or sync_to_async. For more, read
    http://channels.readthedocs.io/en/latest/topics/consumers.html
    """

    ##### WebSocket event handlers

    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        print("============connect============")
        # print("**get scope list**: " + str(self.scope))

        # Are they logged in? (로그인한 사용자만 연결 가능)
        # if self.scope["user"].is_anonymous:
        #     # Reject the connection
        #     await self.close()
        # else:
        #     # Accept the connection
        #     await self.accept()

        await self.accept()
        self.rooms = set()
        # await self.init_room()
        # await self.send_room(content["room"], content["roomtype"], content["message"])

    async def receive_json(self, content):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Messages will have a "command" key we can switch on
        print("============receive_json============")
        print("receive_json_data: " + str(content))
        command = content.get("command", None)  # client에서 보내준 'command' data를 추출
        try:
            if command == "join":
                # Make them join the room
                await self.join_room(content["room"], content["roomtype"])
            elif command == "leave":
                # Leave the room
                await self.leave_room(content["room"], content["roomtype"])
            elif command == "send":
                await self.send_room(content)
        except ClientError as e:
            # Catch any errors and send it back
            await self.send_json({"error": e.code})

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        print("============disconnect============")
        # Leave all the rooms we are still in
        for room_id in list(self.rooms):
            try:
                await self.leave_room(room_id)
            except ClientError:
                pass

    ##### Command helper methods called by receive_json

    # 처음 group_id를 선택했을 때, 기본 topic을 열고 이전 message(100개)를 보낸다
    async def init_room(self):
        """
        Called by receive_json when someone sent a join command.
        """
        print("============init_room============")
        message_path_list = self.scope['path'].strip('/').split('/')
        # api/group/:group_id/
        print("---message path list: " + str(message_path_list))

        group_id = message_path_list[2]

        # Topic list의 첫번째 room_pk는 삭제 불가능한 기본 토픽에 해당한다
        # room_pk = 1
        room = Topic.objects.filter(group_id=group_id).order_by('pk')[0]
        room_pk = room.id
        print("room_pk: " + str(room_pk))

        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        room = await get_room_or_error(room_pk, self.scope["user"], None)
        messages = await get_previous_messages(room_pk, self.scope["user"], "topics")

        # Send a join message if it's turned on
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
            await self.channel_layer.group_send(
                room.group_name,
                {
                    "type": "chat.join",
                    "room_id": room_pk,
                    "username": self.scope["user"].username,
                }
            )
        # Store that we're in the room
        self.rooms.add(room_pk)
        # Add them to the group so they get room messages
        await self.channel_layer.group_add(
            room.group_name,
            self.channel_name,
        )
        # Instruct their client to finish opening the room
        await self.send_json({
            "join": str(room.id),
            "room_id": room.id,
            "title": room.topic_name,
            "message": messages,  # room에 있던 기존의 message
        })

    async def join_room(self, room_id, room_type):
        """
        Called by receive_json when someone sent a join command.
        """
        print("============join_room============")
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        room = await get_room_or_error(room_id, self.scope["user"], room_type)
        messages = await get_previous_messages(room_id, self.scope["user"], room_type)

        # Send a join message if it's turned on
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
            await self.channel_layer.group_send(
                room.group_name,
                {
                    "type": "chat.join",
                    "room_id": room_id,
                    "username": self.scope["user"].username,
                }
            )
        # Store that we're in the room
        self.rooms.add(room_id)
        # Add them to the group so they get room messages
        await self.channel_layer.group_add(
            room.group_name,
            self.channel_name,
        )
        # Instruct their client to finish opening the room
        await self.send_json({
            "join": str(room.id),
            "room_id": room.id,
            # "title": room.topic_name,
            "message": messages,  # room에 있던 기존의 message
        })

    async def leave_room(self, room_id, room_type):
        """
        Called by receive_json when someone sent a leave command.
        """
        print("============leave_room============")
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        room = await get_room_or_error(room_id, self.scope["user"], room_type)
        # Send a leave message if it's turned on
        if settings.NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
            await self.channel_layer.group_send(
                room.group_name,
                {
                    "type": "chat.leave",
                    "room_id": room_id,
                    "username": self.scope["user"].username,
                }
            )
        # Remove that we're in the room
        self.rooms.discard(room_id)
        # Remove them from the group so they no longer get room messages
        await self.channel_layer.group_discard(
            room.group_name,
            self.channel_name,
        )
        # Instruct their client to finish closing the room
        await self.send_json({
            "leave": str(room.id),
        })

    async def send_room(self, content):
        """
        Called by receive_json when someone sends a message to a room.
        """
        print("============send_room============")
        room_type = content['roomtype']
        room_id = content['room']  # 들어온 topic/chatroom의 pk
        sender_id = content['sender']
        message = content['message']
        print("ROOM_ACCESS_DENIED check")
        print(self.rooms)

        # Check they are in this room
        if room_id not in self.rooms:
            raise ClientError("ROOM_ACCESS_DENIED")

        # Get the room and send to the group about it
        room = await get_room_or_error(room_id, self.scope["user"], room_type)

        # 받은 message를 저장한다
        sender_name = await save_message(room_id, sender_id, room_type, message)

        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "chat.message",  # call chat_message method
                "room_id": room_id,
                # "username": self.scope["user"].username,
                "username": sender_name,
                "message": message,
            }
        )

    ##### Handlers for messages sent over the channel layer

    # These helper methods are named by the types we send - so chat.join becomes chat_join
    async def chat_join(self, event):
        """
        Called when someone has joined our chat.
        """
        print("============chat_join============")
        # Send a message down to the client
        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_ENTER,
                "room": event["room_id"],
                "username": event["username"],
            },
        )

    async def chat_leave(self, event):
        """
        Called when someone has left our chat.
        """
        print("============chat_leave============")
        # Send a message down to the client
        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_LEAVE,
                "room": event["room_id"],
                "username": event["username"],
            },
        )

    async def chat_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        print("============chat_message============")
        print(type(self))
        print(dir(self))
        print(type(event))
        print(dir(event))
        # Send a message down to the client
        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_MESSAGE,
                "room": event["room_id"],
                "username": event["username"],
                "message": event["message"],
            },
        )













