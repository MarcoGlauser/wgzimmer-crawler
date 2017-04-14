from rest_framework import viewsets

from room.models import Room

from room.serializers import RoomSerializer


class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer