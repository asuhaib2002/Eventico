from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission
from event_manager.models import Event
from .serializers import EventSerializer

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
