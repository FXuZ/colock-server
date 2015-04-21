from django.db import models
from django.utils import timezone
import os

upload_prefix = 'user_logo'


class User(models.Model):

    def new_filename(instance, filename):
        fn, ext = os.path.splitext(filename)
        newfn = instance.id
        return os.path.join( upload_prefix, "%s%s" % (newfn, ext) )

    cid = models.CharField(max_length=32)
    ukey = models.CharField(max_length=32)
    # authentication key.

    region_num = models.IntegerField()
    phone_num = models.BigIntegerField()
    nickname = models.CharField(max_length=32)
    reg_time = models.DateTimeField(default=timezone.now)
    phone_hash = models.CharField(max_length=32, db_index=True)
    verify_code = models.CharField(max_length=32, default='')
    verified = models.BooleanField(default=False)
    # no () means it's called every time instead of only when loading the model

    user_name = models.CharField(max_length=32)
    user_logo = models.ImageField(upload_to=new_filename, blank=True)

    def __unicode__(self):
        return unicode(self.id)


class Friendship(models.Model):
    # directed
    src_uid = models.IntegerField(default=0)
    dest_uid = models.IntegerField(default=0)
    friendship_type = models.IntegerField(default=1)
    # type0: src blocked dest, type1: src has phone num of dest, type2: src view dest as intimate

