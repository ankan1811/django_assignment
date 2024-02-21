from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notes')
    shared_with = models.ManyToManyField(User, related_name='shared_notes')


class NoteVersionHistory(models.Model):
    note = models.ForeignKey(
        Note, on_delete=models.CASCADE, related_name='version_history')
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    changes = models.TextField()
