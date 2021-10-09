# chat/consumers.py
import json
from quickvote import actions
from asgiref.sync import async_to_sync
from urllib.parse import unquote
from channels.generic.websocket import WebsocketConsumer


class RoomConsumer(WebsocketConsumer):

    def connect(self):
        self.username = unquote(self.scope['url_route']['kwargs']['username'])
        self.room_name = unquote(self.scope['url_route']['kwargs']['room_name'])
        self.room_group_name = 'room_%s' % self.room_name.replace(' ', '_')
        password = unquote(self.scope['url_route']['kwargs']['password'])

        if actions.scenery.if_room_exists(self.room_name):
            actions.connect_room(self.username, self.room_name, password=password)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()
        self.receive(text_data=json.dumps(
            {'command': 'update_user', 'name': self.username, 'ready': False, 'vote': ''}
        ))

    def disconnect(self, close_code):
        # Leave room group
        actions.disconnect_room(self.room_name, self.username)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {'type': 'update_room'}
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data_json = json.loads(text_data)
        command = data_json.get('command')

        if command == 'stop_or_run_room':
            room = actions.scenery.get_room_by_number(self.room_name)
            if data_json.get('admin'):
                if room.started:
                    actions.finalize_votes(self.room_name)
                else:
                    actions.start_votes(self.room_name)
            command = 'update_room'

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {'type': command, **data_json}
        )

    def update_room(self, event):
        room = actions.scenery.get_room_by_number(self.room_name)
        self.send(text_data=json.dumps(room.serialize()))

    def update_user(self, event):
        room = actions.refresh_room(room=self.room_name, user=event)
        self.send(text_data=json.dumps(room.serialize()))

