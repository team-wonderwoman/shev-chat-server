"""
ASGI entrypoint file for default channel layer.

Points to the channel layer configured as "default" so you can point
ASGI applications at "ShevChatServer.asgi:channel_layer" as their channel layer.
"""

### 핸들러 정의

import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ShevChatServer.settings")
django.setup()
application = get_default_application()


## 실행 방법
# daphne -p 8001 ShevChatServer.asgi:application