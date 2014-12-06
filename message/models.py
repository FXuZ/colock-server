from django.db import models


from django.db import models
from django.utils import timezone


class Message(models.Model):
    sender_uid = models.IntegerField()
    receiver_uid = models.IntegerField()
    message_key = models.CharField(max_length=32)
    send_time = models.DateTimeField(timezone.now)
    # no () means it's called every time instead of only when loading the model

    img = models.FileField(upload_to='./send/files/')

    class Meta:
        ordering = ('receiver_uid',)

