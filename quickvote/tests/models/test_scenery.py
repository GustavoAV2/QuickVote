from quickvote.models.scenery import Scenery, Room
from django.test import TestCase


class TestScenery(TestCase):

    def setUp(self) -> None:
        self.standard_room = Room(
                theme='Theme Test',
                password='password_test',
                room_name='Room Test'
            )

    def test_scenery_adding_server(self):
        scenery = Scenery()

        scenery.adding_server(self.standard_room)

        assert self.standard_room in scenery.rooms

    def test_scenery_if_room_exists(self):
        scenery = Scenery()

        scenery.adding_server(self.standard_room)

        self.assertTrue(scenery.if_room_exists(self.standard_room.room_name))
        self.assertFalse(scenery.if_room_exists("Not Rest Room"))

    def test_scenery_get_room_by_number(self):
        scenery = Scenery()

        scenery.adding_server(self.standard_room)
        room = scenery.get_room_by_room_name(self.standard_room.room_name)

        self.assertEqual(room.room_name, self.standard_room.room_name)
