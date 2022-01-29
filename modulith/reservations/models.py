from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Note(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")


def get_user_notes(user):
    return Note.objects.filter()
