from quickvote.models.room import RoomObjects, Room


class Scenery:
    def __init__(self):
        self.rooms = []

    def adding_server(self, room: RoomObjects or Room) -> RoomObjects or Room:
        self.rooms.append(room)
        return room

    def remove_server(self, room: str):
        room = self.get_room_by_room_name(room)
        if room:
            self.rooms.remove(room)

    def if_room_exists(self, room_name: str) -> bool:
        for room in self.rooms:
            if room.room_name == room_name:
                return True
        return False

    def get_room_by_room_name(self, room_name: str) -> RoomObjects or Room:
        if self.if_room_exists(room_name=room_name):
            for room in self.rooms:
                if room.room_name == room_name:
                    return room

    def serialize(self):
        return {
            'rooms': [
                room.serialize_protected() for room in self.rooms
            ]
        }
