from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Note, NoteVersionHistory
from .serializers import NoteSerializer, NoteVersionHistorySerializer


class NoteAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_create_note(self):
        self.client.force_login(self.user)
        data = {'title': 'Test Note', 'content': 'This is a test note.',
                'owner': self.user.id, 'shared_with': []}
        response = self.client.post('/notes/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_note(self):
        note = Note.objects.create(
            title='Test Note', content='This is a test note.', owner=self.user)
        response = self.client.get(f'/notes/{note.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_share_note(self):
        note = Note.objects.create(
            title='Test Note', content='This is a test note.', owner=self.user)
        data = {'users': []}  # Adjust as needed
        response = self.client.post(
            f'/notes/share/{note.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_note(self):
        note = Note.objects.create(
            title='Test Note', content='This is a test note.', owner=self.user)
        data = {'title': 'Updated Test Note',
                'content': 'This is an updated test note.', 'owner': self.user.id, 'shared_with': []}
        response = self.client.put(
            f'/notes/update/{note.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_note_version_history(self):
        note = Note.objects.create(
            title='Test Note', content='This is a test note.', owner=self.user)
        NoteVersionHistory.objects.create(
            note=note, user=self.user, changes='First version')
        response = self.client.get(f'/notes/version-history/{note.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Add more tests for other APIs as needed
