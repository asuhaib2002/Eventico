from rest_framework import serializers
from event_manager.models import Event
from users.api.serializers import UserSerializer

class EventSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    attendees = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Event
        fields = '__all__'