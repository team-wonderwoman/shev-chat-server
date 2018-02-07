"""
ASGI entrypoint file for default channel layer.

Points to the channel layer configured as "default" so you can point
ASGI applications at "multichat.asgi:channel_layer" as their channel layer.
"""

# 핸들러 정의
import os
import channels
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ShevChatServer.settings")
os.environ['DJANGO_SETTINGS_MODULE'] = "ShevChatServer.settings"
channel_layer = channels.asgi.get_channel_layer()

## 실행 방법
# dephne -b 0.0.0.0 -p 8001 chat.asgi:channel_layer
