from .serializer import TaskSerializer, NoteSerializer
from rest_framework import viewsets, generics, response, status
from rest_framework.permissions import BasePermission, IsAuthenticated
from task_app.models import Task, Note


class NotePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        safe_methods = ('DELETE', 'GET')
        if request.method in safe_methods:
            return obj.author == request.user
        else:
            return True


class TaskPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        safe_methods = ('PUT', 'PUTCH', 'DELETE')
        if request.method in safe_methods:
            return obj.created_from == request.user
        # elif request.method == 'POST':
        #     return request.user.is_company_admin
        else:
            return True


class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, TaskPermission]

    def perform_create(self, serializer):
        serializer.save(created_from=self.request.user)


class NoteView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, NotePermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NoteDestroyAPIView(generics.DestroyAPIView):
    queryset = Note.objects.all()
    permission_classes = [IsAuthenticated, NotePermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
