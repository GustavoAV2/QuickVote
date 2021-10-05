# chat/routing.py
from django.urls import re_path, path
from quickvote.consumers import RoomConsumer

websocket_urlpatterns = [
    # re_path(r'^ws/room/(?P<room_name>\w+)/(?P<username>\w+)/$', RoomConsumer),
    path('ws/room/<str:room_name>/<str:username>/', RoomConsumer),
]
