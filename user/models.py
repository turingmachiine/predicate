from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from predicate import settings


class User(AbstractUser):
    queries = models.IntegerField(default=0)
    last_query = models.DateTimeField(null=True, blank=True)
    is_subscriber = models.BooleanField(default=False, blank=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
