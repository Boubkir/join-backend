from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  


@receiver(reset_password_token_created)

def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    subject = 'Reset passwort'
    reset_link = "Please press on the link to reset your password: http://localhost:4200{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    from_email = "Join Team <boubkir.benamar@gmail.com>"
    send_mail(subject,reset_link,from_email,[reset_password_token.user.email])