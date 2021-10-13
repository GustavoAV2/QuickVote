from typing import Dict
from cryptography.fernet import Fernet
from quickvote.models.user import User
from quickvote.models.scenery import Scenery
from quickvote.models.room import Room, RoomObjects
from secrets import compare_digest


class Actions:
    scenery = Scenery()

    def __init__(self):
        key = Fernet.generate_key()
        self.cryptography = Fernet(key)

    def create_room_for_users(self, room: str, theme: str, users=[], password="") -> Room:
        encrypt_password = self.cryptography.encrypt(password.encode()).decode()
        actual_server = self.scenery.adding_server(Room(theme=theme, room_name=room, password=encrypt_password))
        if users:
            for user in users:
                actual_server.add_user_on_the_server(user)
        return actual_server

    def create_room_for_objects(self, room: str, theme: str, objects, users=[], password="") -> Room:
        encrypt_password = self.cryptography.encrypt(password.encode()).decode()
        actual_server = self.scenery.adding_server(
            RoomObjects(theme=theme, room_name=room, objects=objects, password=encrypt_password)
            )
        if users:
            for user in users:
                actual_server.add_user_on_the_server(user)
        return actual_server

    def connect_room(self, username: str, room: str, password: str, admin: bool = False) -> Room:
        if self.scenery.if_room_exists(room):
            if self.login(room, password):
                actual_server: Room = self.scenery.get_room_by_room_name(room)
                user = User(name=username, room=room, admin=admin)
                actual_server.add_user_on_the_server(user)
                return actual_server

    def disconnect_room(self, room: str, name_user: str):
        actual_server: Room = self.scenery.get_room_by_room_name(room)
        actual_server.remove_user_from_server(name_user)
        if not actual_server.users:
            self.scenery.remove_server(actual_server.room_name)
        return actual_server

    def login(self, room: str, password: str):
        actual_server = self.scenery.get_room_by_room_name(room)
        password_correct = self.cryptography.decrypt(actual_server.password.encode()).decode()
        if password[-2:] == '==':
            password = self.cryptography.decrypt(password.encode()).decode()

        if compare_digest(password_correct, password):
            return True
        return False

    def start_votes(self, room: str) -> Room:
        actual_server = self.scenery.get_room_by_room_name(room)
        actual_server.start_server()
        return actual_server

    def finalize_votes(self, room: str) -> Room:
        actual_server = self.scenery.get_room_by_room_name(room)
        actual_server.finish_server()
        return actual_server

    def refresh_room(self, room: str, user: Dict = None, start: bool = False):
        actual_server = self.scenery.get_room_by_room_name(room)
        if user:
            actual_server.update_user(user, clear=start)
        return actual_server
