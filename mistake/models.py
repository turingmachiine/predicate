from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from mistake.analyze.analyze import error_finder
from user.models import User


class Sentence(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)


class Mistake(models.Model):
    type = models.TextField()
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    changed_by_user = models.BooleanField(default=False)

