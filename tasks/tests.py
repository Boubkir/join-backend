import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from tasks.models import Task
from datetime import datetime
from django.utils import timezone




class TaskViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="TestUser")
        self.task_data = {
            'title': 'New Task',
            'description': 'New Description',
            'due_date': '2023-12-31 01:50:00+00:00',
            'user': self.user.id,
        }
        self.task = Task.objects.create(
            title='Existing Task',
            description='Existing Description',
            due_date='2023-12-31 01:50:00+00:00',
            user=self.user
        )

    def test_create_task(self):
        url = reverse('task-list')
        response = self.client.post(url, self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.get(pk=2).title, 'New Task')

    def test_delete_task(self):
        url = reverse('task-detail', args=[self.task.id])
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_update_task(self):
         url = reverse('task-detail', args=[self.task.id])
         data = {
             'title': 'Updated Task',
             'description': 'Updated Description',
             'due_date': '2023-12-31 01:50:00+00:00',
             'user': self.user.id,
         }
         self.client.force_login(self.user)
         response = self.client.put(url, data, format='json')
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.task.refresh_from_db()
         self.assertEqual(self.task.title, 'Updated Task')
         self.assertEqual(self.task.description, 'Updated Description')

