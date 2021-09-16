from quickvote.models.room import RoomObjects, Room


class Scenery:
    def __init__(self):
        self.rooms = []

    def adding_server(self, room: RoomObjects or Room) -> RoomObjects or Room:
        self.rooms.append(room)
        return room

    def if_room_exists(self, number: str) -> bool:
        for room in self.rooms:
            if room.room == number:
                return True
        return False

    def get_room_by_number(self, number: str) -> RoomObjects or Room:
        if self.if_room_exists(number=number):
            for server in self.rooms:
                if server.room == number:
                    return server

    def serialize(self):
        return {
            'rooms': [
                room.serialize() for room in self.rooms
            ]
        }
