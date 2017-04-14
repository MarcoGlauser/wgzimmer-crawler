from rest_framework import serializers

from room.fields import PointField
from room.models import Room


class RoomSerializer(serializers.ModelSerializer):
    location = PointField()

    class Meta:
        model = Room
        fields = '__all__'