from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    category = models.CharField(max_length=30, default=None,null=True)
    category_color = models.CharField(max_length=30, default=None, null=True)
    title = models.CharField(max_length=200, default=None)
    description = models.CharField(max_length=200, blank=True)
    priority = models.CharField(max_length=10,null=True, blank=True,default=0)
    status = models.CharField(max_length=20, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True,default=0)
    assigned_to = models.ManyToManyField(User, related_name="tasks", blank=True)
    sub_tasks = models.JSONField(default=list, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)