from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class Chatroom(models.Model):
    room=models.CharField(max_length=100)
    message=models.TextField()
    posted_date=models.DateTimeField(default=timezone.now)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    

