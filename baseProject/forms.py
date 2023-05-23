from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Room, Topic, Message

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','password']