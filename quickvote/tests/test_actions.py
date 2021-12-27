import copy
import pytest
from django.test import TestCase
from quickvote.actions import Actions
from quickvote.models.user import User


class TestActions(TestCase):

    def setUp(self) -> None:
        self.room = {
            'room': 'Room Test',
            'theme': 'Theme Test',
            'password': 'password_test'
        }
        self.objects = [{
            'name': 'Object Test',
            'description': 'Description test'
        }]

    def test_actions_create_room_for_users(self):
        actions = Actions()
        room = copy.deepcopy(self.room)
        user = User(name='UserTest', room=room.get('room'))

        actions.create_room_for_users(
            room.get('room'), room.get('theme'), [user], room.get('password'),
        )

        self.assertTrue(actions.scenery.get_room_by_room_name(room.get('room')))

    def test_actions_create_room_for_objects(self):
        actions = Actions()
        room = copy.deepcopy(self.room)
        user = User(name='UserTest', room=self.room.get('room'))

        actions.create_room_for_objects(
            room.get('room'), room.get('theme'), self.objects, [user], room.get('password')
        )

        self.assertTrue(actions.scenery.get_room_by_room_name(room.get('room')))

    def test_actions_login(self):
        actions = Actions()
        room = copy.deepcopy(self.room)
        user = User(name='UserTest', room=self.room.get('room'))

        actions.create_room_for_users(
            room.get('room'), room.get('theme'), [user], room.get('password'),
        )
        response_success = actions.login(room.get('room'), room.get('password'))
        response_failed = actions.login(room.get('room'), 'Test Password')

        self.assertTrue(response_success)
        self.assertFalse(response_failed)

    def test_actions_connect_room(self):
        room = copy.deepcopy(self.room)

        actions = Actions()
        username = 'UserTest'

        actions.create_room_for_users(room=room.get('room'), theme=room.get('theme'), password=room.get('password'))

        room = actions.connect_room(username, room.get('room'), room.get('password'))

        self.assertEqual(room.get_user_by_name(username).name, username)

    def test_actions_disconnect_room(self):
        actions = Actions()
        room_content = copy.deepcopy(self.room)
        user = User(name='UserTest', room=room_content.get('room'))

        room = actions.create_room_for_users(
            room_content.get('room'), room_content.get('theme'), [user], room_content.get('password')
        )

        actions.disconnect_room(user.room, user.name)

        self.assertFalse(len(room.users))
        self.assertFalse(actions.scenery.get_room_by_room_name(room.room_name))

    def test_actions_start_votes(self):
        actions = Actions()
        room_content = copy.deepcopy(self.room)
        user = User(name='UserTest', room=room_content.get('room'))

        room = actions.create_room_for_users(
            room=room_content.get('room'), theme=room_content.get('theme'),
            users=[user], password=room_content.get('password'))

        start_user_not_ready = actions.start_votes(room.room_name).started
        user.ready = True
        start_user_ready = actions.start_votes(room.room_name).started

        self.assertFalse(start_user_not_ready)
        self.assertTrue(start_user_ready)

    def test_actions_finalize_votes(self):
        actions = Actions()
        room = copy.deepcopy(self.room)
        user = User(name='UserTest', room=room.get('room'))
        user.ready = True
        room = actions.create_room_for_users(room.get('room'), room.get('theme'),
                                             [user], room.get('password'))

        start_response = actions.start_votes(room.room_name).started
        finished_response = actions.finalize_votes(room.room_name).started

        self.assertTrue(start_response)
        self.assertFalse(finished_response)

    # def test_actions_refresh_room(self):
    #     actions = Actions()
    #     user = User(name='UserTest', room=self.room.get('room'))
    #     actions.create_room_for_users(
    #         self.room.get('room'), self.room.get('theme'), [user], self.room.get('password')
    #     )
    #
    #     user.ready = True
    #     user.vote = user.name
    #     response = actions.refresh_room(room=user.room, user=user.serialize()).serialize()
    #     response_clear = actions.refresh_room(room=user.room, user=user.serialize(), start=True).serialize()

