from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    first_name = models.CharField(max_length=30, default=None)
    last_name = models.CharField(max_length=30, default=None)
    email = models.CharField(max_length=50, default=None)
    phone = models.CharField(max_length=20, default=None)
    color = models.CharField(max_length=20, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
