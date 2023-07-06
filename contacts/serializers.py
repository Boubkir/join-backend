from .models import Contact
from django.contrib.auth.models import User
from rest_framework import serializers


class ContactSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Contact
        fields = '__all__'