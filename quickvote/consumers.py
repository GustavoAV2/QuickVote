# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from quickvote.actions import Actions, User
from channels.generic.websocket import WebsocketConsumer


class RoomConsumer(WebsocketConsumer):
    actions = Actions()

    def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name

        if self.actions.scenery.if_room_exists(self.room_name):
            self.actions.connect_room(self.username, self.room_name)
        else:
            self.actions.create_room_for_users(self.room_name, "Theme",
                                               users=[User(self.username, self.room_name, admin=True)])

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        self.receive(text_data=json.dumps({'name': self.username, 'ready': False, 'vote': ''}))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.actions.disconnect_room(self.room_name, self.username)
        self.receive(text_data=json.dumps({'name': self.username, 'ready': False, 'vote': ''}))

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        ready = text_data_json.get('ready')
        name = text_data_json.get('name')
        vote = text_data_json.get('vote')

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'update_room',
                'room': self.room_name,
                'ready': ready,
                'vote': vote,
                'name': name,
            }
        )

    # Receive message from room group
    def update_room(self, event):
        room = self.actions.refresh_room(room=event.get('room'), user=event)
        # Send message to WebSocket
        self.send(text_data=json.dumps(room.serialize()))
