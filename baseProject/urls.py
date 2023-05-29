from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [

    path('', views.home, name='home'),
    path('room/<str:pk>/<str:msgPk>', views.room, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>', views.deleteRoomAndTopicRelatedIf, name='delete-room'),
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('delete-comment/<str:pk>', views.deleteComment, name='delete-comment'),
    path('profile/<str:pk>', views.userProfile, name='user-profile'),
    path('update-user/', views.updateUser, name='update-user'),
    path('argumentsAkaTopics/',views.argumentsPage,name="arguments"),
    path('messagesFromUsers/',views.usersMessages,name="messages"),
    path('userSearch/',views.userSearch,name="userSearch"),
    path('requestOfFriendShip/<str:pk>',views.requestFriend,name="send_friend_request"),
    path('friends/',views.friends,name="friends"),
    path('delete-friend/<str:pk>',views.deleteFriend,name='delete-friend'),
    path('accept-friend/<str:pk>',views.acceptFriend,name='accept-friend'),
]