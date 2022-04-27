from django.contrib import admin
from .models import Task, Note


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['deadline', 'created_at', 'status', 'pinned_to', 'created_from']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['author', 'created_at']
