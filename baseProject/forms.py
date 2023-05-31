from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Room, Topic, Message,User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['topic','name','description','friendsOnly']
        exclude = ['host','participants']

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','name','surname','email','password1','password2']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['icon','name','surname','username','email','status','showFriendsMessages']

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body','image']

