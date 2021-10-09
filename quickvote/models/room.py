from typing import List, Dict
from quickvote.models.user import User
from quickvote.models.object import Object


class RoomInterface:
    def __init__(self, theme: str, number: str, password: str, users: List[User] = None, type_room: str = "objects"):
        if users is None:
            users = []
        self.theme = theme
        self.type = type_room
        self.password = password
        self.room = number
        self._started = False
        self.users = users

    @property
    def started(self):
        return self._started

    def new_admin(self, index: int = None):
        if self.users:
            self.users[index].change_administrator_status()

    def if_name_exists_in_server(self, name: str) -> bool:
        for user in self.users:
            if user.name == name:
                return True
        return False

    def add_user_on_the_server(self, user: User):
        if not self._started:
            if len(self.users) > 0:
                if not self.if_name_exists_in_server(name=user.name):
                    self.users.append(user)
            else:
                user.change_administrator_status()
                self.users.append(user)
        else:
            return None

    def get_user_by_name(self, name):
        for user in self.users:
            if user.name == name:
                return user

    def update_user(self, data: Dict, clear: bool = False):
        for user in self.users:
            if user.name == data.get('name'):
                user.ready = data.get('ready')
                user.vote = data.get('vote')
                if not clear:
                    self._refresh_votes()
                else:
                    self._clear()

    def remove_user_from_server(self, name: str):
        if self.if_name_exists_in_server(name=name):
            for user in self.users:
                if user.name == name:
                    self.users.remove(user)
                    if user.get_admin_status():
                        self.new_admin(0)

    def start_server(self):
        self._clear(clear_vote_name=True)
        self._started = True
        return self._started

    def finish_server(self):
        self._started = False
        return self._started

    def _clear(self, *args, **kwargs):
        ...

    def _refresh_votes(self, *args, **kwargs):
        ...

    def serialize_protected(self):
        return {
            'room': self.room,
            'type': self.type,
            'users': [user.serialize_protected() for user in self.users],
        }


class Room(RoomInterface):
    def __init__(self, theme: str, password: str, number: str, users: List[User] = None):
        super().__init__(theme=theme, number=number, password=password, users=users, type_room="users")

    def _refresh_votes(self):
        self._clear()
        for user in self.users:
            voted_name = user.vote
            for voted_user in self.users:
                if voted_user.name == voted_name:
                    voted_user.number_of_votes += 1

    def _clear(self, clear_vote_name: bool = False):
        for user in self.users:
            user.number_of_votes = 0
            if clear_vote_name:
                user.vote = None
                if not user.ready:
                    raise IOError

    def serialize(self):
        return {
            'room': self.room,
            'type': self.type,
            'theme': self.theme,
            'started': self._started,
            'users': [user.serialize() for user in self.users]
        }

    def advanced_serialize(self):
        return {
            'room': self.room,
            'type': self.type,
            'theme': self.theme,
            'started': self._started,
            'password': self.password,
            'users': [user.serialize() for user in self.users],
        }


class RoomObjects(RoomInterface):
    def __init__(self, theme: str, password: str, number: str, objects: List, users: List[User] = None):
        super().__init__(theme=theme, password=password, number=number, users=users)
        if objects:
            self.objects = [Object(obj.get('name'), 0, obj.get('description')) for obj in objects]

    def _refresh_votes(self):
        self._clear()
        for user in self.users:
            for obj in self.objects:
                if user.vote == obj.name:
                    obj.number_of_votes += 1

    def _clear(self, clear_vote_name: bool = False):
        if clear_vote_name:
            for user in self.users:
                user.vote = None
                if not user.ready:
                    raise IOError
        for obj in self.objects:
            obj.number_of_votes = 0

    def serialize(self):
        return {
            'room': self.room,
            'type': self.type,
            'theme': self.theme,
            'started': self._started,
            'users': [user.serialize() for user in self.users],
            'objects': [obj.serialize() for obj in self.objects],
        }

    def advanced_serialize(self):
        return {
            'room': self.room,
            'type': self.type,
            'theme': self.theme,
            'started': self._started,
            'password': self.password,
            'users': [user.serialize() for user in self.users],
            'objects': [obj.serialize() for obj in self.objects],
        }
