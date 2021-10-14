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
        username = 'UserTest'

        actions.create_room_for_users(self.room.get('room'), self.room.get('theme'), self.room.get('password'))

        room = actions.connect_room(username, self.room.get('room'), self.room.get('password'))

        assert room.get_user_by_name(username).name == username

    def test_actions_disconnect_room(self):
        actions = Actions()
        user = User(name='UserTest', room=self.room.get('room'))
        room = actions.create_room_for_users(
            self.room.get('room'), self.room.get('theme'), [user], self.room.get('password')
        )

        actions.disconnect_room(user.room, user.name)

        assert not len(room.users)
        assert not actions.scenery.get_room_by_room_name(room.room_name)

    def test_actions_start_votes(self):
        actions = Actions()
        user = User(name='UserTest', room=self.room.get('room'))
        room = actions.create_room_for_users(self.room.get('room'), self.room.get('theme'),
                                             [user], self.room.get('password'))

        start_user_not_ready = actions.start_votes(room.room_name).started
        user.ready = True
        start_user_ready = actions.start_votes(room.room_name).started

        assert not start_user_not_ready
        assert start_user_ready

    def test_actions_finalize_votes(self):
        actions = Actions()
        user = User(name='UserTest', room=self.room.get('room'))
        user.ready = True
        room = actions.create_room_for_users(self.room.get('room'), self.room.get('theme'),
                                             [user], self.room.get('password'))

        start_response = actions.start_votes(room.room_name).started
        finished_response = actions.finalize_votes(room.room_name).started

        assert start_response
        assert not finished_response

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

