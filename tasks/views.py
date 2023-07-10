from .models import Task
from .serializers import TaskSerializer, UserSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.exceptions import PermissionDenied




class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(Q(assigned_to=user) | Q(user=user))
    
    def update(self, request, *args, **kwargs):
        task_id = kwargs['pk']
        try:
            instance = get_object_or_404(Task, pk=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user != instance.user and request.user not in instance.assigned_to.all():
            raise PermissionDenied('You are not authorized to update this task.')

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]