

class User:
    def __init__(self, name, room: str, admin=False, token=None):
        self.name = name
        self.room = room
        self._admin = admin
        self._ready = False
        self.vote = None
        self.number_of_votes = 0

    @property
    def ready(self):
        return self._ready

    @ready.setter
    def ready(self, value):
        if value:
            self._ready = True
        else:
            self._ready = False

    def get_admin_status(self):
        return self._admin

    def voted(self, name):
        self.vote = name

    def adding_votes(self):
        self.number_of_votes += 1

    def removing_votes(self):
        self.number_of_votes -= 1

    def change_administrator_status(self):
        self._admin = not self._admin

    def serialize(self):
        return {
            'name': self.name,
            'admin': self._admin,
            'ready': self._ready,
            'room': self.room,
            'vote': self.vote,
            'number_of_votes': self.number_of_votes
        }
