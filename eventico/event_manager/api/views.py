from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission
from event_manager.models import Event
from .serializers import EventSerializer
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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def attend(self, request, pk=None):
        event = self.get_object()
        if request.user in event.attendees.all():
            return Response({'message': 'You are already attending this event.'}, status=status.HTTP_200_OK)
        event.attendees.add(request.user)
        event.save()
        return Response({'message': 'Successfully added as an attendee.'}, status=status.HTTP_200_OK)