from quickvote.actions import Actions
from quickvote.models.user import User


class TestScenery:
    room = {
        'room': 'Room Test',
        'theme': 'Theme Test',
        'password': 'password_test'
    }
    objects = [{
        'name': 'Object Test',
        'description': 'Description test'
    }]

    def test_actions_create_room_for_users(self):
        actions = Actions()
        user = User(name='UserTest', room=self.room.get('room'))

        actions.create_room_for_users(
            self.room.get('room'), self.room.get('theme'), [user], self.room.get('password'),
        )

        assert actions.scenery.get_room_by_room_name(self.room.get('room'))

    def test_actions_create_room_for_objects(self):
        actions = Actions()
        user = User(name='UserTest', room=self.room.get('room'))

        actions.create_room_for_objects(
            self.room.get('room'), self.room.get('theme'), self.objects, [user], self.room.get('password')
        )

        assert actions.scenery.get_room_by_room_name(self.room.get('room'))

    def test_actions_login(self):
        actions = Actions()
        user = User(name='UserTest', room=self.room.get('room'))

        actions.create_room_for_users(
            self.room.get('room'), self.room.get('theme'), [user], self.room.get('password'),
        )
        response_success = actions.login(self.room.get('room'), self.room.get('password'))
        response_failed = actions.login(self.room.get('room'), 'Test Password')

        assert response_success
        assert not response_failed

    def test_actions_connect_room(self):
        actions = Actions()

    def test_actions_disconnect_room(self):
        actions = Actions()

    def test_actions_start_votes(self):
        actions = Actions()

    def test_actions_finalize_votes(self):
        actions = Actions()

    def test_actions_refresh_room(self):
        actions = Actions()
