from django.db import models
from django.utils import timezone

upload_prefix='upload'


class Message(models.Model):
    sender_uid = models.IntegerField()
    receiver_uid = models.IntegerField()
    message_key = models.CharField(max_length=32)
    send_time = models.DateTimeField(default=timezone.now)
    exist = models.BooleanField(default=True)
    filetype = models.CharField(max_length=10)
    # no () means it's called every time instead of only when loading the model

    img = models.FileField(upload_to=upload_prefix)

    class Meta:
        ordering = ('receiver_uid',)

