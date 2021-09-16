from django.test import TestCase, Client
from django.urls import reverse_lazy


class RoomViewTestCase(TestCase):
    def setUp(self) -> None:
        self.username = 'userTest'
        self.room = 'roomTest'
        self.client = Client()

    def test_room(self):
        request = self.client.post(reverse_lazy(self.room + "/" + self.username))
