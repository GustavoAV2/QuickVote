import uuid
from typing import Dict
from random import randint
from quickvote.models.user import User
from quickvote.models.scenery import Scenery
from quickvote.models.room import Room, RoomObjects


class Actions:
    scenery = Scenery()

    def _create_number_of_room(self):
        while True:
            room_number = str(randint(100000, 999999))
            if not self.scenery.if_room_exists(room_number):
                return room_number

    def create_room_for_users(self, room: str, theme: str, users=[], password="") -> Room:
        try:
            token = uuid.uuid4()
            number_room = self._create_number_of_room()
            actual_server = self.scenery.adding_server(Room(theme=theme, number=room,
                                                            token=token, password=password))
            if users:
                for user in users:
                    actual_server.add_user_on_the_server(user)
            return actual_server
        except KeyError:
            raise IOError()

    def create_room_for_objects(self, room) -> Room:
        try:
            token = uuid.uuid4()
            number_room = self._create_number_of_room()
            actual_server = self.scenery.adding_server(
                RoomObjects(
                    theme=room.theme, number=number_room,  objects=room.objects,
                    token=token, password=room.password
                ))
            return actual_server
        except KeyError:
            raise IOError()

    def connect_room(self, username: str, room: str, admin: bool = False) -> Room:
        if self.scenery.if_room_exists(room):
            actual_server: Room = self.scenery.get_room_by_number(room)
            user = User(name=username, room=room, admin=admin)
            actual_server.add_user_on_the_server(user)
            return actual_server
        else:
            raise IOError()

    def disconnect_room(self, room: str, name_user: str):
        actual_server: Room = self.scenery.get_room_by_number(room)
        actual_server.remove_user_from_server(name_user)
        return actual_server

    def start_votes(self, room: str) -> Room:
        actual_server = self.scenery.get_room_by_number(room)
        actual_server.start_server()
        return actual_server

    def finalize_votes(self, room: str) -> Room:
        actual_server = self.scenery.get_room_by_number(room)
        actual_server.finish_server()
        return actual_server

    def refresh_room(self, room: str, user: Dict = None, start: bool = False):
        actual_server = self.scenery.get_room_by_number(room)
        if user:
            actual_server.update_user(user, clear=start)
        return actual_server
