from django.urls import path
from rest_framework import routers
from task_app.views import TaskView, NoteView, NoteDestroyAPIView, ChangeStatusTaskView

router = routers.DefaultRouter()
router.register(r"task", TaskView, basename="task")
# router.register(r"note", NoteView, basename="note")

urlpatterns = [
    path('note/', NoteView.as_view(), name='note'),
    path('note/delete/<int:pk>', NoteDestroyAPIView.as_view(), name='note-delete'),
    path('task/status/<int:pk>', ChangeStatusTaskView.as_view(), name='change-status-task'),
]

urlpatterns += router.urls
