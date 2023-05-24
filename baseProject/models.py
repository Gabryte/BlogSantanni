from django.db import models
from django.contrib.auth.models import  AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Topic(models.Model):
    name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.name
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    topic = models.ForeignKey(Topic, null=True, blank=True,on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-updated','-created')

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-updated','-created')

    def __str__(self):
        return self.body[0:50]
