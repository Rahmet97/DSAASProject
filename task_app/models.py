from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Task(models.Model):
    status = (
        ('TO_DO', 'TO_DO'),
        ('DOING', 'DOING'),
        ('TESTING', 'TESTING'),
        ('WAITING', 'WAITING'),
        ('DOING', 'DOING'),
        ('DONE', 'DONE'),
        ('HISTORY', 'HISTORY')
    )
    description = models.TextField()
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='TO_DO', choices=status)

    pinned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_pinned_to', null=True, blank=True)
    created_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_from')


class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="note_author")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
