from django.urls import path
from . import views

urlpatterns = [
    path('',views.getRouting),
    path('channels/',views.getChannels),
    path('channels/<str:pk>',views.getChannel)
]