import uuid

from django.db import models
from django.contrib.gis.db import models as gis_models

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    room_identifier = models.CharField(max_length=64, db_index=True, unique=True)
    url = models.CharField(max_length=256)
    street = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    from_date = models.DateField()
    to_date = models.DateField(null=True)
    to_text = models.CharField(max_length=256, null=True)
    location = gis_models.PointField()
    rent = models.IntegerField()
    room_description = models.TextField()
    profile_description = models.TextField()
    mates_description = models.TextField()

    crawled_at = models.DateTimeField(auto_now_add=True)
