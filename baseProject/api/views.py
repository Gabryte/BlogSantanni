from rest_framework.decorators import api_view
from rest_framework.response import Response
from baseProject.models import Room
from .serializers import ChannelSerializer
@api_view(['GET'])
def getRouting(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getChannels(request):
    channels = Room.objects.all()
    serializer = ChannelSerializer(channels,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getChannel(request, pk):
    channels = Room.objects.get(id=pk)
    serializer = ChannelSerializer(channels,many=False)
    return Response(serializer.data)