from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def loginPage(request):
    page ='login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')

    context = {'page':page}
    return render(request, 'baseProject/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('loginPage')

def registerUser(request):
    #if request.user.is_authenticated:
    #    return redirect('home')
    #context={'page':page}
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Account was created for ' + user.username)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error has occurred during registration')
    context = {'form':form}
    return render(request, 'baseProject/login_register.html',context)
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)).order_by('-updated')
    topic = Topic.objects.all()

    rooms_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)) #TODO Modify get all the follower messages
    context = {'rooms':rooms, 'topics':topic, 'rooms_count':rooms_count, 'room_messages':room_messages}
    return render(request, 'baseProject/home.html',context)
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'baseProject/room.html',context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    context = {'user':user, 'rooms':rooms}
    return render(request, 'baseProject/profile.html',context)


@login_required(login_url='loginPage')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'baseProject/room_form.html',context)

@login_required(login_url='loginPage')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'baseProject/room_form.html',context)

@login_required(login_url='loginPage')
def deleteRoom(request, pk):

    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == "POST":
        room.delete()
        return redirect('home')
    context = {'obj':room}
    return render(request, 'baseProject/delete.html',context)


@login_required(login_url='loginPage')
def deleteComment(request, pk):

    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == "POST":
        message.delete()
        return redirect('home')
    context = {'obj':message}
    return render(request, 'baseProject/delete.html',context)