import uuid

from django.db import models
from django.contrib.auth.models import  AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    surname = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True,null=True)
    status = models.TextField(null=True)
    icon = models.ImageField(null=True, default="userBase.svg")
    showFriendsMessages = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    created = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

class Topic(models.Model):
    name = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.name
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    topic = models.ForeignKey(Topic, null=True, blank=True,on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    friendsOnly = models.BooleanField(default=False)
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
    image = models.ImageField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comment')
    class Meta:
        ordering = ('-updated','-created')

    def __str__(self):
        return self.body[0:50]

