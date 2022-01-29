from django.test import TestCase

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from reservations.models import Note


class TestNotesView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_should_return_user_notes(self):
        url = reverse('notes-list')
        user = User.objects.create_user("user", "pwd", "uset@gmail.com")
        Note.objects.create(text="blabla", user=user)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(
            response.json(), [{"text": "blabla", "user": 1}]
        )
