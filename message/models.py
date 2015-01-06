from django.db import models
from django.utils import timezone
import os
from colock.key_generator import message_key_gen

upload_prefix='upload'


class Message(models.Model):
    def new_filename(instance, filename):
        fn, ext = os.path.splitext(filename)
        newfn = message_key_gen( instance.sender_uid,
                instance.receiver_uid, str( instance.send_time ) )
        instance.filetype = ext
        return os.path.join( upload_prefix, "%s%s" % (newfn, ext) )

    sender_uid = models.IntegerField()
    receiver_uid = models.IntegerField()
    message_key = models.CharField(max_length=32)
    send_time = models.DateTimeField(default=timezone.now)
    # no () means it's called every time instead of only when loading the model
    exist = models.BooleanField(default=True)
    filetype = models.CharField(max_length=10, default=".png")

    img = models.ImageField(upload_to=new_filename)

    class Meta:
        ordering = ('receiver_uid',)


class RouterMessage(models.Model):
    sender_uid = models.IntegerField()
    send_time = models.DateTimeField(default=timezone.now)
    exist = models.BooleanField(default=True)
