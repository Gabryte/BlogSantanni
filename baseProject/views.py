from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Topic, Message, User, FriendshipRequest
from .forms import RoomForm, UserForm,UserRegistrationForm
from django.db.models import Q, Count, Sum
from django.contrib.auth.decorators import login_required



# Create your views here.


def loginPage(request):
    page ='login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'Email does not exist')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email or password is incorrect')

    context = {'page':page}
    return render(request, 'baseProject/loginAndRegister.html',context)

def logoutUser(request):
    logout(request)
    return redirect('loginPage')

def registerUser(request):
    #if request.user.is_authenticated:
    #    return redirect('home')
    #context={'page':page}
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
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

def userSearch(request):
    page = 'userSearch'
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    users = User.objects.filter(Q(username__icontains=q) | Q(email__icontains=q) | Q(name__icontains=q) | Q(surname__icontains=q))
    num = 5
    topic = Topic.objects.annotate(num_participants=Count('room__participants'), num_rooms=Count('room')).order_by(
        '-num_participants', '-num_rooms')[0:num]
    total_participants = topic.aggregate(total_participants=Sum('num_participants')).get('total_participants', 0)
    rooms_count = 0
    room_messages = None
    searched_users_messages = Message.objects.filter(Q(user__username__icontains=q) | Q(user__email__icontains=q) | Q(user__name__icontains=q) | Q(user__surname__icontains=q))

    user = request.user
    requestFriendsExists = False
    if user.is_authenticated:
        requestFriendsExists = FriendshipRequest.objects.filter(
            from_user=user,
            accepted=True,
        ).exists()

        if (requestFriendsExists == False):
            requestFriendsExists = FriendshipRequest.objects.filter(
                to_user=user,
                accepted=True,
            ).exists()

        if (requestFriendsExists != False):
            # Get all accepted outgoing friend requests
            outgoing_requests = FriendshipRequest.objects.filter(
                from_user=user,
                accepted=True
            ).values_list('to_user', flat=True)

            # Get all accepted incoming friend requests
            incoming_requests = FriendshipRequest.objects.filter(
                to_user=user,
                accepted=True
            ).values_list('from_user', flat=True)

            # Combine outgoing and incoming requests to get all friends
            friend_ids = set(list(outgoing_requests) + list(incoming_requests))

            # Retrieve the user objects for the friend IDs
            friends = User.objects.filter(id__in=friend_ids)
            friend_messages = Message.objects.filter(user__in=friends)
        else:
            friend_messages = None
    else:
        friend_messages = None

    context = {'searched_users_messages':searched_users_messages,'users':users,'topics': topic, 'rooms_count': rooms_count, 'room_messages': room_messages, "num": num,
               "total_participants": total_participants, "friend_messages": friend_messages, "page": page,"requestFriendsExists":requestFriendsExists}
    return render(request, 'baseProject/home.html', context)

def home(request):
    page = 'home'
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)).order_by('-updated')
    num = 5
    topic = Topic.objects.annotate(num_participants=Count('room__participants'), num_rooms=Count('room')).order_by('-num_participants', '-num_rooms')[0:num]
    total_participants = topic.aggregate(total_participants=Sum('num_participants')).get('total_participants', 0)
    rooms_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    user = request.user
    requestFriendsExists = False
    if user.is_authenticated:

        requestFriendsExists = FriendshipRequest.objects.filter(
            from_user=user,
            accepted=True,
        ).exists()

        if(requestFriendsExists == False):
            requestFriendsExists = FriendshipRequest.objects.filter(
                to_user=user,
                accepted=True,
            ).exists()

        if(requestFriendsExists != False):
            # Get all accepted outgoing friend requests
            outgoing_requests = FriendshipRequest.objects.filter(
                from_user=user,
                accepted=True
            ).values_list('to_user', flat=True)

            # Get all accepted incoming friend requests
            incoming_requests = FriendshipRequest.objects.filter(
                to_user=user,
                accepted=True
            ).values_list('from_user', flat=True)

            # Combine outgoing and incoming requests to get all friends
            friend_ids = set(list(outgoing_requests) + list(incoming_requests))

            # Retrieve the user objects for the friend IDs
            friends = User.objects.filter(id__in=friend_ids)
            friend_messages = Message.objects.filter(user__in=friends)
        else:
            friend_messages = None
    else:
        friend_messages = None

    context = {'rooms':rooms, 'topics':topic, 'rooms_count':rooms_count, 'room_messages':room_messages,"num":num,"total_participants":total_participants,"friend_messages":friend_messages,"page":page,"requestFriendsExists":requestFriendsExists}
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
    page = 'userProfile'
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()

    num = 5
    topics = Topic.objects.annotate(num_participants=Count('room__participants'), num_rooms=Count('room')).order_by(
        '-num_participants', '-num_rooms')[0:num]
    total_participants = topics.aggregate(total_participants=Sum('num_participants')).get('total_participants', 0)

    userSearched = user
    userRequester = request.user

    can_send = not FriendshipRequest.objects.filter(
        from_user=userRequester,
        to_user=userSearched,
    ).exists()

    context = {'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics,"num":num,"total_participants":total_participants,"page":page,"can_send":can_send}
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
def deleteRoomAndTopicRelatedIf(request, pk):

    room = Room.objects.get(id=pk)
    topic = room.topic
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == "POST":
        room.delete()
        if (topic.room_set.count() == 0):
            topic.delete()
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
        return redirect('home')#TODO CHANGE
    context = {'obj':message}
    return render(request, 'baseProject/delete.html',context)

@login_required(login_url='loginPage')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'baseProject/update-user.html',{'form':form})


def usersMessages(request):
    channel_messages = Message.objects.all()[0:3]
    return render(request, 'baseProject/messagesFromBlogging.html',{'room_messages':channel_messages})


def argumentsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    arguments = Topic.objects.filter(name__icontains=q).annotate(num_rooms=Count('room')).order_by('-num_rooms')
    context={'arguments':arguments}
    return render(request,'baseProject/arguments.html',context)


def requestFriend(request,pk):
    recipient_user = get_object_or_404(User,id=pk)
    sender_user = request.user

    friendship_request = FriendshipRequest.objects.create(
        from_user=sender_user,
        to_user=recipient_user,
    )

    return redirect('user-profile',pk=recipient_user.id)