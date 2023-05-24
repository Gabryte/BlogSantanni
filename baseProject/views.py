from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm
from django.db.models import Q, Count
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
    return render(request, 'baseProject/loginAndRegister.html',context)

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
            messages.error(request, 'Username already exists or the password given does not match the password creation criteria')
    context = {'form':form}
    return render(request, 'baseProject/loginAndRegister.html',context)
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)).order_by('-updated')
    topic = Topic.objects.annotate(num_rooms=Count('room')).order_by('-num_rooms')[0:4]

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
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'baseProject/profile.html',context)


@login_required(login_url='loginPage')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)#Creates the topic if doesn't find the topic
        #form = RoomForm(request.POST)
        #if form.is_valid():
        #    room = form.save(commit=False)
        #    room.host = request.user
        #    room.save()
        #    return redirect('home')
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    context = {'form':form, 'topics':topics}
    return render(request, 'baseProject/room_form.html',context)

@login_required(login_url='loginPage')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)  # Creates the topic if doesn't find the topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.topic = topic
        room.save()
        return redirect('home')
    context = {'form':form, 'topics':topics, 'room':room}
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

@login_required(login_url='loginPage')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'baseProject/update-user.html',{'form':form})

def argumentsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    arguments = Topic.objects.filter(name__icontains=q)
    context={'arguments':arguments}
    return render(request,'baseProject/arguments.html',context)