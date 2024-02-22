from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Note, NoteVersionHistory
from .serializers import NoteSerializer, NoteVersionHistorySerializer


class NoteAPITestCase(TestCase):
    def test_registration(self):
        data = {'username': 'testuser',
                'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post('/signup/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post('/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure token is returned in the response
        self.assertIn('token', response.data)
        # Retrieve the token and set it as a property of the test case class
        self.token = response.data['token']

    def test_create_note(self):
        data = {'title': 'Test Note', 'content': 'This is a test note.',
                'owner': self.user.id, 'shared_with': []}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post('/notes/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_note(self):
        note = Note.objects.create(
            title='Test Note', content='This is a test note.', owner=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(f'/notes/{note.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_share_note(self):
        note = Note.objects.create(
            title='Test Note', content='This is a test note.', owner=self.user)
        data = {'users': []}  # Adjust as needed
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(
            f'/notes/share/{note.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_note(self):
        note = Note.objects.create(
            title='Test Note', content='This is a test note.', owner=self.user)
        data = {'title': 'Updated Test Note',
                'content': 'This is an updated test note.', 'owner': self.user.id, 'shared_with': []}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.put(
            f'/notes/update/{note.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_note_version_history(self):
        note = Note.objects.create(
            title='Test Note', content='This is a test note.', owner=self.user)
        NoteVersionHistory.objects.create(
            note=note, user=self.user, changes='First version')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(f'/notes/version-history/{note.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
