import pytest
from quickvote.models.room import Room
from quickvote.models.scenery import Scenery


class TestScenery:
    @pytest.fixture()
    def scenery(self):
        scenery = Scenery()
        return scenery

    @pytest.fixture()
    def room(self):
        name = 'TestRoom'
        theme = 'Test-Theme'
        password = 'test'
        return Room(theme, password, name)

    def test_scenery_adding_server(self, scenery, room):
        scenery.adding_server(room=room)

        room_add = scenery.get_room_by_number(room.room)

        assert room_add.room == room.room
