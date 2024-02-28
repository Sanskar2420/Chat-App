from email.policy import default
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as gis_model


User = get_user_model()

# Create your models here.
class Room(models.Model):
    room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(null=True, blank=True)
    participant = models.ManyToManyField(User, related_name='chat')
    is_group_chat = models.BooleanField(default=False)


class Messages(gis_model.Model):
    sender = gis_model.ForeignKey(User, related_name='message_sender', on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete = models.SET_NULL, null=True, blank=True)
    # read_by = gis_model.ManyToManyField(User, related_name='message_read_by')
    message = gis_model.TextField(null=True, blank=True)
    location = gis_model.PointField(null=True, blank=True)
    is_deleted = gis_model.BooleanField(default=False)
    # media = gis_model.FileField()