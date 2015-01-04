from django.db import models
from django.utils import timezone
import os
from colock.key_generator import message_key_gen

upload_prefix='upload'


class Message(models.Model):
    @staticmethod
    def new_filename(self, filename):
        fn, ext = os.path.splitext(filename)
        newfn = message_key_gen(self.sender_uid,
                self.receiver_uid, str( self.send_time ) )
        self.filetype = ext
        return "%s/%s.%s" % ( upload_prefix, newfn, ext )

    sender_uid = models.IntegerField()
    receiver_uid = models.IntegerField()
    message_key = models.CharField(max_length=32)
    send_time = models.DateTimeField(default=timezone.now)
    exist = models.BooleanField(default=True)
    # filetype = models.CharField(max_length=10)
    # no () means it's called every time instead of only when loading the model

    img = models.ImageField(upload_to=new_filename)

    class Meta:
        ordering = ('receiver_uid',)

