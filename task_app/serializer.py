from rest_framework import serializers
from .models import Task, Note


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'description', 'deadline', 'status', 'pinned_to', 'created_at']


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'description', 'created_at']
