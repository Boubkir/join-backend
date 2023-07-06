from .models import Task
from .serializers import TaskSerializer, UserSerializer
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from django.db.models import Q


class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(Q(user=user) | Q(assigned_to=user)).order_by("id")



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
