from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Contact
from contacts.models import Contact
import users

class ContactViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="TestUser")
        self.contact_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'color': 'blue',
            'user': self.user.id,
        }
        self.contact = Contact.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com',
            phone='9876543210',
            color='red',
            user=self.user
        )

    def test_create_contact(self):
        url = reverse('contact-list')
        self.client.force_login(self.user)
        response = self.client.post(url, self.contact_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 2)
        self.assertEqual(Contact.objects.get(pk=2).first_name, 'John')

    def test_delete_contact(self):
        url = reverse('contact-detail', args=[self.contact.id])
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 0)

    def test_update_contact(self):
        url = reverse('contact-detail', args=[self.contact.id])
        data = {
            'first_name': 'Updated First Name',
            'last_name': 'Updated Last Name',
            'email': 'updated.email@example.com',
            'phone': '9999999999',
            'color': 'green',
            'user': self.user.id,
        }
        self.client.force_login(self.user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.first_name, 'Updated First Name')
        self.assertEqual(self.contact.last_name, 'Updated Last Name')

