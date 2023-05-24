from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Room, Topic, Message,User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ['host','participants']

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1','password2']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['icon','name','username','email','status','showFriendsMessages']

