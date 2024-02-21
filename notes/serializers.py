
# serializers.py
from rest_framework import serializers
from .models import Note, NoteVersionHistory


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class NoteVersionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteVersionHistory
        fields = '__all__'
