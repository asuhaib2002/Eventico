from rest_framework import serializers
from event_manager.models import Event
from users.api.serializers import UserSerializer

class EventSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    attendees = UserSerializer(read_only=True,many=True)
    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        validated_data['owner'] = self.context['request'].user
        attendees_data = validated_data.pop('attendees', [])
        print(attendees_data)
        # return super().create(validated_data)

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['owner']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user        
        return super().create(validated_data)
