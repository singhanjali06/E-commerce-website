from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Welcome!',
            f'Hi {instance.username}, thanks for registering with us!',
            None,
            [instance.email],
            fail_silently=False,
        )