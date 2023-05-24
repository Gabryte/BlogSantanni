from rest_framework.serializers import ModelSerializer
from baseProject.models import Room

class ChannelSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'