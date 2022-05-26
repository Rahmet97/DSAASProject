from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, response, status
from rest_framework.permissions import BasePermission, IsAuthenticated
from task_app.models import Task, Note
from rest_framework.views import APIView
from django.http import Http404
from rest_framework_simplejwt import exceptions, authentication, tokens

from .serializer import TaskSerializer, NoteSerializer, TaskStatusSerializer


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
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated, TaskPermission]

    def perform_create(self, serializer):
        serializer.save(created_from=self.request.user)


class ChangeStatusTaskView(generics.GenericAPIView):
    serializer_class = TaskStatusSerializer
    queryset = Task.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated, TaskPermission]

    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializers = self.get_serializer(task, request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return response.Response(status=200)


class NoteView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated, NotePermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NoteDestroyAPIView(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated, NotePermission]

    def get_object(self, pk):
        try:
            return Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        note = self.get_object(pk)
        note.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
