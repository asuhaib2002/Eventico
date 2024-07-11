from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission
from event_manager.models import Event
from .serializers import EventSerializer, EventCreateSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().select_related('owner').prefetch_related('attendees')
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method in ['GET']:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid():
            attendees_data = serializer.validated_data.pop('attendees', [])
            event = Event.objects.create(owner=request.user, **serializer.validated_data)
            event.attendees.set(attendees_data)
            event.save()
            return Response(EventSerializer(event).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def attend(self, request, pk=None):
        event = self.get_object()
        if request.user in event.attendees.all():
            return Response({'message': 'You are already attending this event.'}, status=status.HTTP_200_OK)
        event.attendees.add(request.user)
        event.save()
        return Response({'message': 'Successfully added as an attendee.'}, status=status.HTTP_200_OK)