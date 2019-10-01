from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class Chatroom(models.Model):
    room=models.CharField(max_length=100)
    message=models.TextField()

    def __str__(self):
        return str(self.message)
    

class Loggeduser(models.Model):
    username=models.CharField(max_length=100)
    
