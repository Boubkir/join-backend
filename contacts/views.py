from contacts.models import Contact
from .serializers import ContactSerializer
from rest_framework import viewsets,permissions
from rest_framework.authentication import TokenAuthentication

class ContactView(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    # authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user).order_by("id")