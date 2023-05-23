from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Room, Topic, Message

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['host','name', 'topic', 'description']

