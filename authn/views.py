from tasks.serializers import UserSerializer
from .serializers import RegisterSerializer
from rest_framework import permissions, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from knox.models import AuthToken
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.views import APIView
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from knox.views import LoginView
from rest_framework import permissions,status


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')
        email = request.data.get('email')

        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        user.set_password(password)

        user.save()

        subject = "Willkommen bei Join"
        message = "Hallo {},\n\nWillkommen bei unserer App! Vielen Dank für die Registrierung.".format(
            user.username
        )
        from_email = "Join Team <boubkir.benamar@gmail.com>"
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)
        
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )
        
        
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        response = super(LoginAPI, self).post(request, format=None)
        response.data["user"] = UserSerializer(user).data
        return response
    
class EmailLoginAPI(LoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        User = get_user_model()
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if email is None or password is None:
            return Response({'error': 'Bitte geben Sie Ihre E-Mail-Adresse und Ihr Passwort ein.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Ungültige Anmeldeinformationen.'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({'error': 'Ungültige Anmeldeinformationen.'}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)

        response = super().post(request, format=None)
        response.data["user"] = UserSerializer(user).data
        return response



class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({"message": "Logged out successfully"})


class PasswordResetView(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')
        print(f"Email: {email}")
        user = User.objects.filter(email=email).first()
        if user:
            print(f"User PK: {user.pk}")
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            from_email = "Join Team <boubkir.benamar@gmail.com>"
            subject = 'Reset password'
            reset_link = f"http://localhost:4200/reset-password-confirm/{uidb64}/{token}/"
            send_mail(
                subject,
                f'Bitte klicken Sie auf den folgenden Link, um Ihr Passwort zurückzusetzen: {reset_link}',
                from_email,
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Password reset email sent'})
        return Response({'message': 'User not found'}, status=400)

      
      
class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token, format=None):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'message': 'Invalid reset link'}, status=400)

        token_generator = PasswordResetTokenGenerator()
        if token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            if new_password:
                user.password = make_password(new_password)
                user.save()
                return Response({'message': 'Password reset successful'})
            return Response({'message': 'New password is required'}, status=400)
        return Response({'message': 'Invalid reset link'}, status=400)