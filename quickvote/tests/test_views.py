from quickvote import actions
from django.urls import reverse_lazy, reverse
from django.test import TestCase, Client


class IndexViewTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_index(self):
        request = self.client.get(reverse_lazy('home'))

        self.assertEqual(request.status_code, 200)

        self.assertTrue(request.context_data.get('api_url'))


class RoomViewTestCase(TestCase):
    username = 'userTest'
    room = 'roomTest'

    def setUp(self) -> None:
        self.client = Client()

    def test_room(self):
        data = {
            'room_name': self.room,
            'username': self.username,
            'password': self.username + self.room
        }
        actions.create_room_for_users(self.room, "Test Theme", password=data.get('password'))

        request = self.client.get(reverse('room', kwargs=data))

        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.context_data.get('room_name'), self.room)
        self.assertEqual(request.context_data.get('username'), self.username)
        self.assertEqual(request.context_data.get('password'), data.get('password'))


class FastLoginTestCase(TestCase):
    username = 'userTest'
    room = 'roomTest'

    def setUp(self) -> None:
        self.client = Client()

    def test_fast_login(self):
        room = actions.create_room_for_users(self.room, "Test Theme", password=self.username + self.room)
        data = {
            'room_name': self.room,
            'password': room.password
        }
        request = self.client.get(reverse_lazy('fast-login', kwargs=data))

        self.assertEqual(request.status_code, 200)

        self.assertTrue(request.context_data.get('api_url'))
        self.assertEqual(request.context_data.get('room_name'), self.room)
        self.assertEqual(request.context_data.get('password'), data.get('password'))
