import pytest
from quickvote.models.scenery import Scenery, Room


class TestScenery:

    @pytest.fixture()
    def standard_room(self):
        return Room(
            theme='Theme Test',
            password='password_test',
            room_name='Room Test'
        )

    def test_scenery_adding_server(self, standard_room):
        scenery = Scenery()

        scenery.adding_server(standard_room)

        assert standard_room in scenery.rooms

    def test_scenery_if_room_exists(self, standard_room):
        scenery = Scenery()

        scenery.adding_server(standard_room)

        assert scenery.if_room_exists(standard_room.room_name)
        assert not scenery.if_room_exists("Not Rest Room")

    def test_scenery_get_room_by_number(self, standard_room):
        scenery = Scenery()

        scenery.adding_server(standard_room)
        room = scenery.get_room_by_room_name(standard_room.room_name)

        assert room.room_name == standard_room.room_name
